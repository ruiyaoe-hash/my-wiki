# -*- coding: utf-8 -*-
"""Protocol Executor v0.3 — template-aware, fail-fast, full handler coverage.

Supports {{inputs.key}} and {{steps.N.key}} template resolution, plus the
literal {date} placeholder (replaced with today's ISO date).
Missing handlers abort the protocol (return False) instead of silently
skipping, so a protocol can no longer fake success.
"""
import sys, os, json, re, urllib.request
from datetime import datetime, date, timezone
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'state_manager'))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'event_bus'))
PROTOCOL_DIR = Path(__file__).resolve().parent.parent / 'protocol'
BASE_DIR = Path(__file__).resolve().parent.parent

def llm_summarize(text):
    """Optional LLM-backed summarizer (OpenAI-compatible chat completions).

    Active only when both AGENT_RUNTIME_LLM_BASE_URL and
    AGENT_RUNTIME_LLM_API_KEY env vars are set; model comes from
    AGENT_RUNTIME_LLM_MODEL (default 'gpt-4o-mini'). Returns the summary
    text, or None when not configured or the call failed (caller should
    fall back to the extractive summary). Stdlib only (urllib).
    """
    base_url = os.environ.get('AGENT_RUNTIME_LLM_BASE_URL')
    api_key = os.environ.get('AGENT_RUNTIME_LLM_API_KEY')
    if not base_url or not api_key: return None
    model = os.environ.get('AGENT_RUNTIME_LLM_MODEL', 'gpt-4o-mini')
    payload = json.dumps({
        'model': model,
        'messages': [
            {'role': 'system', 'content': '你是摘要助手，用中文输出结构化 Markdown 摘要（要点列表）。'},
            {'role': 'user', 'content': f'请为以下内容生成摘要：\n\n{text[:8000]}'}
        ]
    }).encode('utf-8')
    req = urllib.request.Request(base_url.rstrip('/') + '/chat/completions', data=payload,
                                 headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {api_key}'})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        return data['choices'][0]['message']['content']
    except Exception as e:
        print(f'  LLM summary failed, falling back to extractive: {e}')
        return None


class ProtocolExecutor:
    def __init__(self): self.state = {}; self.context = {}
    def load(self, protocol_id):
        path = PROTOCOL_DIR / f'{protocol_id}.json'
        if not path.exists(): return None
        with open(path, 'r', encoding='utf-8') as f: return json.load(f)
    def _resolve(self, value, step_outputs):
        if not isinstance(value, str): return value
        value = re.sub(r'\{\{inputs\.(\w+)\}\}', lambda m: str(self.context.get(m.group(1), m.group(0))), value)
        value = re.sub(r'\{\{steps\.(\d+)\.(\w+)\}\}', lambda m: str(step_outputs.get(int(m.group(1)), {}).get(m.group(2), m.group(0))), value)
        # Literal {date} (not part of a {{...}} template) -> today's ISO date
        value = re.sub(r'(?<!\{)\{date\}(?!\})', date.today().isoformat(), value)
        return value
    def execute(self, protocol_id, inputs=None):
        proto = self.load(protocol_id)
        if not proto: print(f'Not found: {protocol_id}'); return False
        self.context = inputs or {}
        print(f'{proto["protocol_id"]} v{proto["version"]}: {proto["description"]}')
        step_outputs = {}
        for step in proto.get('steps', []):
            sid = step['id']; action = step['action']
            params = {k: self._resolve(v, step_outputs) for k, v in step.get('params', {}).items()}
            desc = step.get('description', action)
            try:
                handler = getattr(self, f'_handle_{action}', None)
                if not handler:
                    print(f'  [{sid}] ERROR: no handler for action "{action}" — aborting protocol')
                    self.state[sid] = {'success': False, 'error': f'no handler: {action}'}
                    return False
                print(f'  [{sid}] {desc}...')
                result = handler(params)
                self.state[sid] = {'success': True, 'result': result}
                step_outputs[sid] = result
            except Exception as e: self.state[sid] = {'success': False, 'error': str(e)}; print(f'  FAILED: {e}'); return False
        print(f'Protocol {protocol_id} completed.'); return True
    def _handle_search_files(self, p):
        d = BASE_DIR / p['dir']; files = list(d.glob(p.get('pattern', '*')))
        return {'count': len(files), 'files': [str(f.relative_to(BASE_DIR)) for f in files]}
    def _handle_check_stale(self, p):
        d = BASE_DIR / 'knowledge'; threshold = p.get('threshold_days', 90); stale = []
        for f in d.glob('*.json'):
            if f.name == 'metadata-schema.json': continue
            with open(f, 'r', encoding='utf-8') as fp: sc = json.load(fp)
            try:
                dt = datetime.strptime(sc.get('updated', '2026-01-01'), '%Y-%m-%d').date()
                age = (date.today() - dt).days
                if age > threshold: stale.append({'id': sc['knowledge_id'], 'title': sc['title'], 'age_days': age})
            except: pass
        return {'stale_count': len(stale), 'stale_items': stale[:10]}
    def _handle_call_manager(self, p):
        from manager import StateManager; sm = StateManager(); m = p['method']
        if m == 'read': return sm.read(p['file'])
        if m == 'write': return sm.write(p['file'], p['data'], 'Executor')
        if m == 'update':
            current = sm.read(p['file'])
            if not isinstance(current, dict): current = {}
            merged = {**current, **(p.get('data') or {})}
            return sm.write(p['file'], merged, 'Executor')
        if m == 'health_check': return sm.health_check()
        if m == 'get_goal':
            task = sm.read('current-task.json') or {}
            return task.get('context') or {}
        return {'error': f'Unknown: {m}'}
    def _handle_generate_report(self, p):
        output = p.get('output', 'reports/report.md')
        out_path = BASE_DIR / output; out_path.parent.mkdir(parents=True, exist_ok=True)
        lines = [f'# Report — {datetime.now(timezone.utc).isoformat()}', '']
        for sid, r in self.state.items(): lines.append(f'- Step {sid}: {"OK" if r.get("success") else "FAIL"}')
        with open(out_path, 'w', encoding='utf-8') as f: f.write('\n'.join(lines))
        return {'report_path': str(output)}
    def _handle_fetch_url(self, p):
        url = p.get('url', ''); output_dir = BASE_DIR / p.get('output_dir', 'source/original/'); output_dir.mkdir(parents=True, exist_ok=True)
        if os.path.isfile(url):
            src = Path(url); dest = output_dir / src.name
            with open(src, 'r', encoding='utf-8') as f: content = f.read()
            with open(dest, 'w', encoding='utf-8') as f: f.write(content)
        elif url.startswith('http'):
            req = urllib.request.Request(url, headers={'User-Agent': 'AgentRuntime/1.0'})
            with urllib.request.urlopen(req, timeout=15) as resp: content = resp.read().decode('utf-8', errors='replace')
            fname = url.rstrip('/').split('/')[-1] or 'index'
            if not fname.endswith(('.md','.txt','.html','.json')): fname += '.html'
            dest = output_dir / fname
            with open(dest, 'w', encoding='utf-8') as f: f.write(content)
        else: raise ValueError(f'Unsupported: {url}')
        return {'original_path': str(dest.relative_to(BASE_DIR)), 'size_chars': len(content)}
    def _handle_generate_summary(self, p):
        input_file = BASE_DIR / p.get('input_file', ''); output_dir = BASE_DIR / p.get('output_dir', 'source/summaries/'); output_dir.mkdir(parents=True, exist_ok=True)
        if not input_file.exists(): raise FileNotFoundError(str(input_file))
        with open(input_file, 'r', encoding='utf-8') as f: content = f.read()
        wc = len(content.split())
        llm_text = llm_summarize(content)
        if llm_text is not None:
            body = f'- 生成方式: LLM ({os.environ.get("AGENT_RUNTIME_LLM_MODEL", "gpt-4o-mini")})\n\n{llm_text}\n'
        else:
            body = '- 生成方式: 提取式（未配置 LLM）\n\n## 要点\n\n' + self._extractive_summary(content)
        dest = output_dir / f'{input_file.stem}_summary.md'
        header = f'# 摘要\n\n- 来源: {input_file.name}\n- 字数: {len(content)} 字符\n'
        with open(dest, 'w', encoding='utf-8') as f: f.write(header + body)
        return {'summary_path': str(dest.relative_to(BASE_DIR)), 'word_count': wc, 'method': 'llm' if llm_text is not None else 'extractive'}
    def _extractive_summary(self, content):
        """Structural summary: title + each level-1/2 heading with its first 1-2 sentences."""
        title = ''; sections = []; cur = None
        for line in content.splitlines():
            m = re.match(r'^(#{1,2})\s+(.+?)\s*$', line)
            if m:
                if len(m.group(1)) == 1 and not title: title = m.group(2)
                cur = {'heading': m.group(2), 'body': []}; sections.append(cur)
            elif cur is not None:
                cur['body'].append(line)
        lines = []
        if title: lines.append(f'- 标题: {title}')
        for s in sections:
            text = ' '.join(l.strip() for l in s['body'] if l.strip() and not l.strip().startswith(('#', '>', '|')))
            sents = [x for x in re.split(r'(?<=[。！？.!?])\s*', text) if x.strip()][:2]
            excerpt = ' '.join(sents)[:200]
            lines.append(f'- **{s["heading"]}**' + (f': {excerpt}' if excerpt else ''))
        return '\n'.join(lines) + '\n'
    def _handle_create_knowledge_page(self, p):
        title = p.get('title', 'Untitled'); domain = p.get('domain', 'knowledge-management'); output_dir = BASE_DIR / p.get('output_dir', '知识库/'); output_dir.mkdir(parents=True, exist_ok=True)
        tags_raw = p.get('tags', []); tags = [t.strip() for t in tags_raw.split(',')] if isinstance(tags_raw, str) else (tags_raw if isinstance(tags_raw, list) else [])
        today = date.today().isoformat(); tags_s = '\n'.join(f'- {t}' for t in tags) if tags else '- pending'
        fname = title.replace(' ', '_').replace('/', '_').replace(':', '-') + '.md'; dest = output_dir / fname
        # 入库铁律：知识页必须声明来源（frontmatter source）并回链源材料（## 来源 小节）
        source_stem = Path(p['source_path']).stem if p.get('source_path') else None
        source_fm = f'source: "{source_stem}"\n' if source_stem else ''
        source_sec = f'\n## 来源\n\n- [[{source_stem}]]\n' if source_stem else ''
        page = f'---\ntitle: "{title}"\ncreated: "{today}"\nupdated: "{today}"\ntype: concept\ndomain: {domain}\nstatus: draft\n{source_fm}tags:\n{tags_s}\n---\n\n# {title}\n\n> Agent Runtime ingest 协议自动生成。\n{source_sec}'
        with open(dest, 'w', encoding='utf-8-sig') as f: f.write(page)
        return {'page_path': str(dest.relative_to(BASE_DIR)), 'title': title}
    def _handle_generate_sidecar(self, p):
        page_path = BASE_DIR / p.get('page_path', ''); output_dir = BASE_DIR / p.get('output_dir', 'knowledge/'); output_dir.mkdir(parents=True, exist_ok=True)
        if not page_path.exists(): raise FileNotFoundError(str(page_path))
        with open(page_path, 'r', encoding='utf-8-sig') as f: content = f.read()
        links = list(set(re.findall(r'\[\[([^\]|#]+)(?:[#|][^\]]+)?\]\]', content)))
        sc = {'knowledge_id': page_path.stem.replace(' ', '_').lower(), 'title': page_path.stem, 'path': str(page_path.relative_to(BASE_DIR)), 'created': date.today().isoformat(), 'updated': date.today().isoformat(), 'type': 'concept', 'domain': 'knowledge-management', 'status': 'draft', 'tags': [], 'source_refs': [], 'dependencies': [], 'outgoing_links': links, 'freshness_score': 1.0}
        fn = page_path.stem.replace(' ', '_').replace('?', '').replace(':', '-').lower() + '.json'; dest = output_dir / fn
        with open(dest, 'w', encoding='utf-8') as f: json.dump(sc, f, ensure_ascii=False, indent=2)
        return {'sidecar_path': str(dest.relative_to(BASE_DIR))}
    def _handle_update_index(self, p):
        title = p.get('new_page_title', 'New Page'); ip = BASE_DIR / 'index.md'
        if not ip.exists(): return {'updated': False}
        with open(ip, 'r', encoding='utf-8') as f: content = f.read()
        content = content.replace('## 新入库\n', f'## 新入库\n- [[{title}]] — Agent Runtime 自动入库\n')
        with open(ip, 'w', encoding='utf-8') as f: f.write(content)
        return {'updated': True}
    def _handle_emit_event(self, p):
        from event_bus import get_bus, Event; bus = get_bus()
        ev = Event(p.get('event_type', 'custom'), p.get('payload', {})); bus.emit(ev)
        return {'event_id': ev.id, 'type': ev.type}
    def _handle_update_hot_md(self, p):
        """Idempotently replace (or append) the '## 最近会话' section in hot.md
        with a summary of the current session from state/session.json +
        state/current-task.json."""
        from manager import StateManager; sm = StateManager()
        session = sm.read('session.json') or {}
        task = sm.read('current-task.json') or {}
        summary = (task.get('context') or {}).get('summary', '')
        now = datetime.now(timezone.utc).isoformat()
        new_section = (
            '## 最近会话\n\n'
            f'- 会话: {session.get("session_id", "unknown")}\n'
            f'- 状态: {session.get("status", "unknown")}\n'
            f'- 任务: {task.get("task_id") or "(无)"} — {summary}\n'
            f'- 更新时间: {now}\n'
        )
        hot_path = BASE_DIR / 'hot.md'
        content = hot_path.read_text(encoding='utf-8') if hot_path.exists() else ''
        pattern = re.compile(r'## 最近会话\n.*?(?=\n## |\Z)', re.S)
        if pattern.search(content):
            content = pattern.sub(lambda _: new_section.rstrip('\n'), content, count=1)
            if not content.endswith('\n'): content += '\n'
        else:
            content = content.rstrip('\n') + ('\n\n' if content.strip() else '') + new_section
        hot_path.write_text(content, encoding='utf-8')
        return {'updated': True, 'session_id': session.get('session_id')}
    def _handle_append_log(self, p):
        """Append one ISO-timestamped line to p['file'] (e.g. log.md). Append-only."""
        fname = p.get('file', 'log.md')
        message = p.get('message')
        if not message:
            from manager import StateManager; sm = StateManager()
            session = sm.read('session.json') or {}
            task = sm.read('current-task.json') or {}
            message = f'wrapup: 会话 {session.get("session_id", "unknown")}（{session.get("status", "unknown")}），任务 {task.get("task_id") or "(无)"}（{task.get("status", "unknown")}）'
        path = BASE_DIR / fname
        line = f'- [{datetime.now(timezone.utc).isoformat()}] {message}\n'
        with open(path, 'a', encoding='utf-8') as f: f.write(line)
        return {'appended': True, 'file': fname}
    def _handle_write_next_plan(self, p):
        """(Re)write the next-session plan file: progress summary, re-entry
        steps (read session.json -> hot.md -> confirm direction), candidates."""
        fname = p.get('file') or '下次工作计划.md'
        if re.search(r'[<>:"/\\|?*]', fname):  # Windows-invalid chars (e.g. mojibake '?') — fall back
            print(f'  invalid filename {fname!r}, falling back to 下次工作计划.md')
            fname = '下次工作计划.md'
        from manager import StateManager; sm = StateManager()
        session = sm.read('session.json') or {}
        task = sm.read('current-task.json') or {}
        summary = (task.get('context') or {}).get('summary', '')
        candidates = p.get('candidates') or ['（占位）下次会话确认优先级']
        lines = [
            f'# 下次工作计划 — {date.today().isoformat()}',
            '',
            '## 当前进度',
            f'- 会话: {session.get("session_id", "unknown")}（{session.get("status", "unknown")}）',
            f'- 任务: {task.get("task_id") or "(无)"}，进度 {task.get("progress", 0)} — {summary}',
            '',
            '## 下次进站操作',
            '1. 读 state/session.json',
            '2. 读 hot.md',
            '3. 确认方向',
            '',
            '## 候选任务',
        ]
        lines += [f'- {c}' for c in candidates]
        path = BASE_DIR / fname
        path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
        return {'written': fname, 'candidates': len(candidates)}
    def _handle_check_threshold(self, p):
        """Grade p['value'] against warn/limit/hard_cut thresholds."""
        value = float(p.get('value', 0) or 0)
        warn = float(p.get('warn', 50000)); limit = float(p.get('limit', 100000)); hard = float(p.get('hard_cut', 200000))
        if value >= hard: level = 'hard_cut'
        elif value >= limit: level = 'limit'
        elif value >= warn: level = 'warn'
        else: level = 'ok'
        return {'level': level, 'value': value}
    def _handle_emit_warning(self, p):
        """Print a warning and emit Event('agent.warning', payload) on the bus."""
        payload = p.get('payload')
        if not isinstance(payload, dict):
            payload = {'message': str(payload)} if payload else {}
        if p.get('condition'): payload.setdefault('condition', p['condition'])
        print(f'  WARNING: {payload or "(no payload)"}')
        from event_bus import get_bus, Event; bus = get_bus()
        ev = Event('agent.warning', payload, source='executor'); bus.emit(ev)
        return {'event_id': ev.id, 'type': ev.type}

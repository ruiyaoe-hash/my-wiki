# -*- coding: utf-8 -*-
"""Protocol Executor v0.2 — template-aware, full handler coverage.

Supports {{inputs.key}} and {{steps.N.key}} template resolution.
"""
import sys, os, json, re, urllib.request
from datetime import datetime, date, timezone
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'state-manager'))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'event-bus'))
PROTOCOL_DIR = Path(__file__).resolve().parent.parent / 'protocol'
BASE_DIR = Path(__file__).resolve().parent.parent

class ProtocolExecutor:
    def __init__(self): self.state = {}; self.context = {}
    def load(self, protocol_id):
        path = PROTOCOL_DIR / f'{protocol_id}.json'
        if not path.exists(): return None
        with open(path, 'r', encoding='utf-8') as f: return json.load(f)
    def _resolve(self, value, step_outputs):
        if not isinstance(value, str) or '{{' not in value: return value
        value = re.sub(r'\{\{inputs\.(\w+)\}\}', lambda m: str(self.context.get(m.group(1), m.group(0))), value)
        value = re.sub(r'\{\{steps\.(\d+)\.(\w+)\}\}', lambda m: str(step_outputs.get(int(m.group(1)), {}).get(m.group(2), m.group(0))), value)
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
                if not handler: print(f'  [{sid}] SKIP {action}'); self.state[sid] = {'success': False}; continue
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
        if m == 'health_check': return sm.health_check()
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
        wc = len(content.split()); preview = content[:500].replace('\n', ' ').strip()
        dest = output_dir / f'{input_file.stem}_summary.md'
        with open(dest, 'w', encoding='utf-8') as f: f.write(f'# Summary\n\nSource: {input_file.name}\nChars: {len(content)}\n\n{preview}...\n')
        return {'summary_path': str(dest.relative_to(BASE_DIR)), 'word_count': wc}
    def _handle_create_knowledge_page(self, p):
        title = p.get('title', 'Untitled'); domain = p.get('domain', 'knowledge-management'); output_dir = BASE_DIR / p.get('output_dir', '知识库/'); output_dir.mkdir(parents=True, exist_ok=True)
        tags_raw = p.get('tags', []); tags = [t.strip() for t in tags_raw.split(',')] if isinstance(tags_raw, str) else (tags_raw if isinstance(tags_raw, list) else [])
        today = date.today().isoformat(); tags_s = '\n'.join(f'- {t}' for t in tags) if tags else '- pending'
        fname = title.replace(' ', '_').replace('/', '_').replace(':', '-') + '.md'; dest = output_dir / fname
        page = f'---\ntitle: "{title}"\ncreated: "{today}"\nupdated: "{today}"\ntype: concept\ndomain: {domain}\nstatus: draft\ntags:\n{tags_s}\n---\n\n# {title}\n\n> Agent Runtime ingest 协议自动生成。\n'
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

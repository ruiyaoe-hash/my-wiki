# -*- coding: utf-8 -*-
"""网页控制台（v1.3.0 Step 2）— 本地网页操作界面。

架构：纯 Python 标准库 http.server，只监听 127.0.0.1（本机单人使用）。
本身零业务逻辑，是 Step 1 结构化命令层上面的一层薄壳：

- 按钮区从 protocol/*.json 声明式生成，一个协议一个按钮，
  点按钮等价于替你敲对应的 `agent-runtime <子命令> --json`
- 健康总览来自 `agent-runtime status --json` 同一份数据（cli._collect_status）
- ingest 等需要参数的协议配表单，不用记命令行参数

写操作保护（按钮会真实改库，三层）：
1. 前端二次确认（confirm 弹窗）
2. 操作日志：每次点击追加落盘 state/console-log.jsonl
3. 全局执行锁：同一时刻只跑一个协议，且底层走 StateManager 既有锁

启动：`agent-runtime console [--port 8765]`
"""

import io
import json
import sys
import threading
import webbrowser
from contextlib import redirect_stdout
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
for _d in ('agents', 'planner', 'executor', 'state_manager', 'event_bus', 'memory'):
    _p = str(BASE / _d)
    if _p not in sys.path:
        sys.path.insert(0, _p)

import cli  # noqa: E402  # Step 1 命令层，控制台的所有能力都来自它

PROTOCOL_DIR = BASE / 'protocol'
LOG_FILE = BASE / 'state' / 'console-log.jsonl'
EVENTS_FILE = BASE / 'event_bus' / 'history' / 'events.jsonl'
MAX_BODY = 64 * 1024  # POST 体上限 64KB，够用且防滥用

# 协议 -> 命令层 argv 的映射。没有映射的协议（如 auto 触发的
# context-budget）在页面上展示为"仅自动触发"，不生成可点按钮。
COMMAND_MAP = {
    'check': lambda p: ['check', '--json'],
    'wrapup': lambda p: ['wrapup', '--json'],
    'ingest': lambda p: ['ingest', p.get('url_or_path', ''),
                         '--title', p.get('title', ''),
                         '--domain', p.get('domain', 'knowledge-management'),
                         '--tags', p.get('tags', ''), '--json'],
}
# ingest 的表单字段声明，页面据此渲染表单
FORM_FIELDS = {
    'ingest': [
        {'name': 'url_or_path', 'label': 'URL 或本地文件路径', 'required': True},
        {'name': 'title', 'label': '知识页标题', 'required': True},
        {'name': 'domain', 'label': 'domain', 'required': False,
         'default': 'knowledge-management'},
        {'name': 'tags', 'label': '标签（逗号分隔）', 'required': False},
    ],
}

_run_lock = threading.Lock()


def list_protocols():
    """从 protocol/*.json 生成按钮清单（声明式，加协议自动出现）。"""
    items = []
    for p in sorted(PROTOCOL_DIR.glob('*.json')):
        if p.name == 'TEMPLATE.json':
            continue
        try:
            data = json.loads(p.read_text(encoding='utf-8'))
        except (OSError, json.JSONDecodeError):
            continue
        pid = data.get('protocol_id', p.stem)
        items.append({
            'id': pid,
            'description': data.get('description', ''),
            'runnable': pid in COMMAND_MAP,
            'form': FORM_FIELDS.get(pid),
        })
    return items


def recent_events(n=8):
    """最近 n 条已落盘事件（读 events.jsonl 尾部）。"""
    if not EVENTS_FILE.exists():
        return []
    lines = EVENTS_FILE.read_text(encoding='utf-8').splitlines()
    events = []
    for line in lines[-n:]:
        try:
            e = json.loads(line)
            events.append({'type': e.get('type', '?'),
                           'source': e.get('source', ''),
                           'time': e.get('timestamp', e.get('time', ''))})
        except json.JSONDecodeError:
            events.append({'type': line[:80], 'source': '', 'time': ''})
    return list(reversed(events))


def read_log(n=20):
    """最近 n 条控制台操作日志。"""
    if not LOG_FILE.exists():
        return []
    lines = LOG_FILE.read_text(encoding='utf-8').splitlines()
    entries = []
    for line in lines[-n:]:
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return list(reversed(entries))


def _append_log(entry):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open('a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')


def run_protocol(protocol_id, params):
    """替你敲命令：走 Step 1 命令层，全程持全局锁，结果落操作日志。"""
    build = COMMAND_MAP.get(protocol_id)
    if build is None:
        return {'rc': 2, 'error': '协议不可从控制台运行: {}'.format(protocol_id)}
    argv = build(params or {})
    if protocol_id == 'ingest' and (not argv[1] or not params.get('title')):
        return {'rc': 2, 'error': 'ingest 需要 url_or_path 与 title'}
    with _run_lock:
        buf = io.StringIO()
        try:
            with redirect_stdout(buf):
                rc = cli.main(argv)
        except SystemExit as e:  # argparse 参数错误会 SystemExit(2)
            rc = e.code if isinstance(e.code, int) else 2
        except Exception as e:  # 协议异常不外泄成 500，记进日志并返回
            rc = 1
            buf.write('\n[console] exception: {}'.format(e))
        out = buf.getvalue()
    entry = {'ts': datetime.now(timezone.utc).isoformat(),
             'protocol': protocol_id, 'params': params or {},
             'argv': argv, 'rc': rc}
    _append_log(entry)
    try:
        result = json.loads(out)
    except json.JSONDecodeError:
        result = {'raw': out}
    return {'rc': rc, 'result': result}


PAGE = """<!doctype html>
<html lang="zh">
<head>
<meta charset="utf-8">
<title>Agent Runtime 控制台</title>
<style>
 body{font-family:system-ui,"Microsoft YaHei",sans-serif;max-width:960px;
      margin:24px auto;padding:0 16px;color:#222;background:#fafafa}
 h1{font-size:20px} h2{font-size:15px;margin:20px 0 8px;color:#555}
 .card{background:#fff;border:1px solid #e2e2e2;border-radius:8px;
       padding:12px 16px;margin-bottom:12px}
 .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));
       gap:8px}
 .stat{font-size:13px}.stat b{display:block;font-size:18px;margin-top:2px}
 button{cursor:pointer;border:1px solid #3b6ea5;background:#3b6ea5;color:#fff;
        border-radius:6px;padding:8px 14px;font-size:14px;margin:4px 6px 4px 0}
 button:disabled{background:#ccc;border-color:#ccc;cursor:not-allowed}
 .desc{font-size:12px;color:#777;margin-bottom:4px}
 input{width:100%;box-sizing:border-box;padding:6px;margin:2px 0 8px;
       border:1px solid #ccc;border-radius:4px;font-size:13px}
 label{font-size:12px;color:#555}
 pre{background:#2d2d2d;color:#ddd;padding:10px;border-radius:6px;
     font-size:12px;overflow:auto;max-height:300px;white-space:pre-wrap}
 ul{margin:4px 0;padding-left:18px;font-size:13px}
 .ok{color:#2a7d2a}.bad{color:#b03030}
</style>
</head>
<body>
<h1>Agent Runtime 控制台 <button onclick="loadStatus()">刷新</button></h1>

<h2>健康总览</h2>
<div class="card grid" id="health">加载中…</div>

<h2>操作（点按钮 = 替你敲命令，会真实改库）</h2>
<div class="card" id="actions">加载中…</div>

<h2>执行结果</h2>
<div class="card"><pre id="result">（还没有运行过）</pre></div>

<h2>最近事件</h2>
<div class="card"><ul id="events"></ul></div>

<h2>最近操作日志</h2>
<div class="card"><ul id="oplog"></ul></div>

<script>
async function loadStatus(){
  try{
    const r = await fetch('/api/status'); const s = await r.json();
    const e = s.execution||{}, c = s.report_counts||{}, ses = s.session||{};
    document.getElementById('health').innerHTML =
      stat('会话', (ses.session_id||'?')+'（'+(ses.status||'?')+'）') +
      stat('累计任务', (e.tasks_processed??0)+' 个 / '+(e.sessions_total??0)+' 会话') +
      stat('待办队列', (s.planner?s.planner.queue_size:0)+' 个') +
      stat('落盘事件', (s.events_persisted??0)+' 条') +
      stat('stale 页', c.stale_count??'?') +
      stat('断链', c.broken_count??'?') +
      stat('已核实', (s.epistemic?(s.epistemic.by_verification.verified||0)+'/'+s.epistemic.total:'?')) +
      stat('最新报告', s.latest_report||'无');
    const ev = document.getElementById('events');
    ev.innerHTML = (s.recent_events||[]).map(x =>
      '<li>'+esc(x.time)+' · '+esc(x.type)+' · '+esc(x.source)+'</li>').join('') ||
      '<li>（无）</li>';
    const ar = await fetch('/api/protocols'); const ps = await ar.json();
    document.getElementById('actions').innerHTML = ps.map(renderAction).join('');
    loadLog();
  }catch(err){
    document.getElementById('health').innerHTML =
      '<b style="color:#b03030">连不上后台服务了</b><div class="stat">'+
      '网页只是脸面，发动机（控制台服务）没在跑。'+
      '双击仓库里的「启动控制台.bat」，或终端执行 agent-runtime console，'+
      '然后按 Ctrl+F5 强制刷新本页。（'+esc(String(err))+'）</div>';
    document.getElementById('actions').innerHTML = '';
  }
}
function stat(k,v){return '<div class="stat">'+esc(k)+'<b>'+esc(String(v))+'</b></div>';}
function esc(s){const d=document.createElement('div');d.textContent=s;return d.innerHTML;}
function renderAction(p){
  let h = '<div style="margin-bottom:10px"><div class="desc">'+esc(p.id)+' · '+esc(p.description)+'</div>';
  if(!p.runnable) return h+'<button disabled>仅自动触发</button></div>';
  if(p.form){
    h += p.form.map(f => '<label>'+esc(f.label)+(f.required?' *':'')+
      '</label><input id="f_'+p.id+'_'+f.name+'" value="'+(f.default||'')+'">').join('');
  }
  h += '<button onclick="run(\\''+p.id+'\\','+(p.form?'true':'false')+')">运行 '+esc(p.id)+'</button></div>';
  return h;
}
async function run(id, hasForm){
  if(!confirm('确定运行 '+id+'？这会真实改动知识库/状态。')) return;
  const params = {};
  if(hasForm){
    for(const el of document.querySelectorAll('[id^="f_'+id+'_"]')){
      params[el.id.slice(id.length+3)] = el.value;
    }
  }
  show('运行中…（协议可能要几秒）');
  const r = await fetch('/api/run', {method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({protocol:id, params:params})});
  const data = await r.json();
  show((data.rc===0?'✓ 成功':'✗ 失败 rc='+data.rc)+'\\n\\n'+
       JSON.stringify(data.result??data, null, 2));
  loadStatus();
}
function show(t){
  const el = document.getElementById('result'); el.textContent = t;
}
async function loadLog(){
  const r = await fetch('/api/log'); const ls = await r.json();
  document.getElementById('oplog').innerHTML = ls.map(x =>
    '<li>'+esc(x.ts)+' · '+esc(x.protocol)+' · rc='+x.rc+'</li>').join('') ||
    '<li>（无）</li>';
}
loadStatus();
</script>
</body>
</html>
"""


class ConsoleHandler(BaseHTTPRequestHandler):
    """路由：GET / 页面，GET /api/* 只读数据，POST /api/run 执行协议。"""

    server_version = 'AgentRuntimeConsole/1.3'

    def _send(self, code, body, ctype='application/json; charset=utf-8'):
        data = body.encode('utf-8') if isinstance(body, str) else body
        self.send_response(code)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _json(self, obj, code=200):
        self._send(code, json.dumps(obj, ensure_ascii=False, default=str))

    def do_GET(self):
        path = self.path.split('?', 1)[0]
        if path == '/':
            self._send(200, PAGE, 'text/html; charset=utf-8')
        elif path == '/api/status':
            s = cli._collect_status()
            s['recent_events'] = recent_events()
            self._json(s)
        elif path == '/api/protocols':
            self._json(list_protocols())
        elif path == '/api/log':
            self._json(read_log())
        else:
            self._json({'error': 'not found'}, 404)

    def do_POST(self):
        path = self.path.split('?', 1)[0]
        if path != '/api/run':
            self._json({'error': 'not found'}, 404)
            return
        try:
            length = int(self.headers.get('Content-Length') or 0)
        except ValueError:
            length = 0
        if length <= 0 or length > MAX_BODY:
            self._json({'error': 'bad body'}, 400)
            return
        try:
            body = json.loads(self.rfile.read(length).decode('utf-8'))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._json({'error': 'bad json'}, 400)
            return
        protocol = body.get('protocol', '')
        result = run_protocol(protocol, body.get('params') or {})
        self._json(result, 200 if result.get('rc') == 0 else 400)

    def log_message(self, fmt, *args):  # 访问日志保持精简，不刷 stderr
        sys.stderr.write('[console] %s\n' % (fmt % args))


def make_server(port):
    return ThreadingHTTPServer(('127.0.0.1', port), ConsoleHandler)


def serve(port=8765, open_browser=True):
    """起服务。端口被占就顺延找下一个，最多试 10 个。"""
    httpd = None
    for candidate in range(port, port + 10):
        try:
            httpd = make_server(candidate)
            break
        except OSError:
            continue
    if httpd is None:
        print('控制台启动失败：{} 起连续 10 个端口都被占用'.format(port))
        return 1
    url = 'http://127.0.0.1:{}/'.format(httpd.server_address[1])
    print('控制台已启动: {} （只监听本机，Ctrl+C 停止）'.format(url))
    if open_browser:
        webbrowser.open(url)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\n控制台已停止')
    finally:
        httpd.server_close()
    return 0

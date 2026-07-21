# -*- coding: utf-8 -*-
"""网页控制台测试（console/server.py）。

用 ephemeral 端口起真实 HTTP 服务，覆盖：页面可达、/api/status、
/api/protocols（声明式按钮清单）、/api/log、POST /api/run 跑真实
wrapup 协议（触碰文件全部备份恢复）、未知协议与坏请求体的 400。
"""

import json
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
import urllib.request
import urllib.error
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import helpers

sys.path.insert(0, str(helpers.BASE_DIR))
from console import server  # noqa: E402

BASE = helpers.BASE_DIR


class ConsoleTestBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.httpd = server.make_server(0)  # 端口 0 = 系统分配空闲端口
        cls.port = cls.httpd.server_address[1]
        cls.thread = threading.Thread(target=cls.httpd.serve_forever,
                                      daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()
        cls.thread.join(timeout=5)

    def get(self, path):
        with urllib.request.urlopen(
                'http://127.0.0.1:{}{}'.format(self.port, path),
                timeout=10) as r:
            return r.status, r.read().decode('utf-8')

    def post(self, path, payload):
        req = urllib.request.Request(
            'http://127.0.0.1:{}{}'.format(self.port, path),
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}, method='POST')
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.status, json.loads(r.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read().decode('utf-8'))


class TestPagesAndApis(ConsoleTestBase):
    def test_index_page(self):
        status, body = self.get('/')
        self.assertEqual(status, 200)
        self.assertIn('Agent Runtime 控制台', body)
        self.assertIn('/api/run', body)

    def test_status_api(self):
        status, body = self.get('/api/status')
        self.assertEqual(status, 200)
        data = json.loads(body)
        for key in ('session', 'execution', 'planner',
                    'events_persisted', 'recent_events'):
            self.assertIn(key, data)

    def test_protocols_api(self):
        status, body = self.get('/api/protocols')
        self.assertEqual(status, 200)
        items = {p['id']: p for p in json.loads(body)}
        # 三个核心协议必须声明式出现，且 check/wrapup 可运行
        for pid in ('check', 'ingest', 'wrapup'):
            self.assertIn(pid, items)
        self.assertTrue(items['check']['runnable'])
        self.assertTrue(items['wrapup']['runnable'])
        # ingest 带表单声明
        self.assertTrue(items['ingest']['form'])
        # TEMPLATE 不出现
        self.assertNotIn('TEMPLATE', items)

    def test_log_api(self):
        status, body = self.get('/api/log')
        self.assertEqual(status, 200)
        self.assertIsInstance(json.loads(body), list)

    def test_404(self):
        try:
            self.get('/no-such-path')
            self.fail('expected 404')
        except urllib.error.HTTPError as e:
            self.assertEqual(e.code, 404)


class TestRunApi(ConsoleTestBase):
    def setUp(self):
        self.files = [BASE / 'hot.md', BASE / 'log.md', BASE / '下次工作计划.md',
                      BASE / 'state' / 'session.json', server.LOG_FILE]
        self.backups = {p: helpers.backup_file(p) for p in self.files}

    def tearDown(self):
        for path, data in self.backups.items():
            helpers.restore_file(path, data)

    def test_run_wrapup(self):
        code, data = self.post('/api/run', {'protocol': 'wrapup', 'params': {}})
        self.assertEqual(code, 200)
        self.assertEqual(data['rc'], 0)
        # 操作日志追加落盘
        logs = server.read_log()
        self.assertTrue(any(l.get('protocol') == 'wrapup' for l in logs))
        # 协议真实生效：session 翻转为 ended
        session = json.loads((BASE / 'state' / 'session.json').read_text(encoding='utf-8'))
        self.assertEqual(session['status'], 'ended')

    def test_run_unknown_protocol_rejected(self):
        code, data = self.post('/api/run', {'protocol': 'no-such', 'params': {}})
        self.assertEqual(code, 400)
        self.assertNotEqual(data.get('rc'), 0)

    def test_run_ingest_requires_params(self):
        code, data = self.post('/api/run', {'protocol': 'ingest', 'params': {}})
        self.assertEqual(code, 400)
        self.assertNotEqual(data.get('rc'), 0)


class TestPageJavaScript(unittest.TestCase):
    """页面内联 JS 必须能通过语法检查（防 && / ?? 裸混这类
    整个脚本块挂掉的错误；HTML/接口测试抓不到它）。"""

    def test_inline_script_syntax(self):
        node = shutil.which('node')
        if not node:
            self.skipTest('node 不可用，跳过 JS 语法检查')
        m = re.search(r'<script>(.*?)</script>', server.PAGE, re.S)
        self.assertIsNotNone(m, 'PAGE 里没有 script 块')
        tmp = tempfile.NamedTemporaryFile(
            'w', suffix='.js', delete=False, encoding='utf-8')
        try:
            with tmp as f:
                f.write(m.group(1))
            r = subprocess.run([node, '--check', tmp.name],
                               capture_output=True, text=True)
            self.assertEqual(r.returncode, 0,
                             'PAGE 内联 JS 语法错误: ' + r.stderr)
        finally:
            Path(tmp.name).unlink(missing_ok=True)


if __name__ == '__main__':
    unittest.main()

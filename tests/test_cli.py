# -*- coding: utf-8 -*-
"""CLI 命令层测试（agents/cli.py）。

覆盖：argv 归一化（旧式调用映射 run 子命令）、status 子命令
（人读输出 + --json）、check 子命令端到端（真实跑 check 协议，
所有触碰的状态文件备份后恢复，新生成的报告文件用完删除）。
"""

import io
import json
import sys
import unittest
import uuid
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import helpers

sys.path.insert(0, str(helpers.BASE_DIR / 'agents'))
import cli  # noqa: E402

BASE = helpers.BASE_DIR


def run_cli(argv):
    """跑 cli.main 并捕获 stdout，返回 (exit_code, output)。"""
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = cli.main(argv)
    return rc, buf.getvalue()


class TestNormalizeArgv(unittest.TestCase):
    def test_bare_maps_to_run(self):
        self.assertEqual(cli._normalize_argv([]), ['run'])

    def test_old_flags_map_to_run(self):
        self.assertEqual(cli._normalize_argv(['--loop', '3', '--recover']),
                         ['run', '--loop', '3', '--recover'])

    def test_subcommand_untouched(self):
        self.assertEqual(cli._normalize_argv(['status', '--json']),
                         ['status', '--json'])

    def test_help_untouched(self):
        self.assertEqual(cli._normalize_argv(['--help']), ['--help'])


class TestStatusCommand(unittest.TestCase):
    def test_human_readable(self):
        rc, out = run_cli(['status'])
        self.assertEqual(rc, 0)
        self.assertIn('会话', out)
        self.assertIn('队列', out)
        self.assertIn('最新检查', out)

    def test_json_output(self):
        rc, out = run_cli(['status', '--json'])
        self.assertEqual(rc, 0)
        data = json.loads(out)
        for key in ('session', 'execution', 'planner',
                    'events_persisted', 'latest_report'):
            self.assertIn(key, data)


class TestCheckCommand(unittest.TestCase):
    def setUp(self):
        state_files = [BASE / 'state' / n for n in
                       ('task-queue.json', 'current-task.json',
                        'session.json', 'execution-status.json')]
        self.backups = {p: helpers.backup_file(p) for p in state_files}
        # 隔离 session id，避免归档撞真实运行的会话
        self.session_file = BASE / 'state' / 'session.json'
        self.test_session = 'test-cli-{}'.format(uuid.uuid4().hex[:8])
        self.session_file.write_text(json.dumps({
            'session_id': self.test_session, 'status': 'active',
            'agent': 'TestCLI'
        }, ensure_ascii=False, indent=2), encoding='utf-8')
        self.archive = BASE / 'memory' / 'sessions' / (self.test_session + '.json')
        self.archive_backup = helpers.backup_file(self.archive)
        # 报告与事件历史按真实运行追加，全部备份恢复
        self.reports_dir = BASE / 'reports'
        self.reports_before = {p.name for p in self.reports_dir.glob('check-*.md')}
        self.report_backups = {p: helpers.backup_file(p)
                               for p in self.reports_dir.glob('check-*.md')}
        self.events = BASE / 'event_bus' / 'history' / 'events.jsonl'
        self.events_backup = helpers.backup_file(self.events)

    def tearDown(self):
        for path, data in self.backups.items():
            helpers.restore_file(path, data)
        helpers.restore_file(self.archive, self.archive_backup)
        for path, data in self.report_backups.items():
            helpers.restore_file(path, data)
        for p in self.reports_dir.glob('check-*.md'):
            if p.name not in self.reports_before:
                p.unlink()
        helpers.restore_file(self.events, self.events_backup)

    def test_check_json(self):
        rc, out = run_cli(['check', '--json'])
        self.assertEqual(rc, 0)
        data = json.loads(out)
        self.assertTrue(data['ok'])
        self.assertTrue(data['report'].startswith('reports/check-'))
        self.assertIsNotNone(data['stale_count'])
        self.assertIsNotNone(data['broken_count'])

    def test_check_human_readable(self):
        rc, out = run_cli(['check'])
        self.assertEqual(rc, 0)
        self.assertIn('检查完成', out)
        self.assertIn('断链', out)


class TestIngestCommandFailure(unittest.TestCase):
    """ingest 走真实协议但不落产物：源文件不存在，第一步即失败，
    验证 cli 的参数传递与退出码（成功路径已由 test_executor_ingest 覆盖）。"""

    def test_missing_source_returns_1(self):
        rc, out = run_cli(['ingest', 'no_such_file_xyz.md', '--title', 'X'])
        self.assertEqual(rc, 1)
        self.assertIn('ingest FAILED', out)

    def test_missing_source_json(self):
        rc, out = run_cli(['ingest', 'no_such_file_xyz.md', '--title', 'X', '--json'])
        self.assertEqual(rc, 1)
        data = json.loads(out)
        self.assertFalse(data['ok'])


class TestWrapupCommand(unittest.TestCase):
    """wrapup 子命令端到端：跑真实协议，备份恢复所有触碰文件。"""

    def setUp(self):
        self.files = [BASE / 'hot.md', BASE / 'log.md', BASE / '下次工作计划.md',
                      BASE / 'state' / 'session.json']
        self.backups = {p: helpers.backup_file(p) for p in self.files}

    def tearDown(self):
        for path, data in self.backups.items():
            helpers.restore_file(path, data)

    def test_wrapup_ok(self):
        rc, out = run_cli(['wrapup'])
        self.assertEqual(rc, 0)
        self.assertIn('wrapup OK', out)
        session = json.loads((BASE / 'state' / 'session.json').read_text(encoding='utf-8'))
        self.assertEqual(session['status'], 'ended')

    def test_wrapup_json(self):
        rc, out = run_cli(['wrapup', '--json'])
        self.assertEqual(rc, 0)
        data = json.loads(out)
        self.assertTrue(data['ok'])


if __name__ == '__main__':
    unittest.main()

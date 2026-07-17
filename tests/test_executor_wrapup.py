# -*- coding: utf-8 -*-
"""Executor 'wrapup' protocol test.

Exercises the call_manager 'update' fix (step 4 must merge
{"status": "ended"} into session.json instead of overwriting it).
Backs up and restores every real working file the protocol touches:
hot.md, log.md, 下次工作计划.md, state/session.json.
"""

import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import helpers

from executor import ProtocolExecutor

BASE = helpers.BASE_DIR


class TestExecutorWrapup(unittest.TestCase):
    def setUp(self):
        self.hot = BASE / 'hot.md'
        self.log = BASE / 'log.md'
        self.plan = BASE / '下次工作计划.md'
        self.session = BASE / 'state' / 'session.json'
        self.backups = {p: helpers.backup_file(p) for p in
                        (self.hot, self.log, self.plan, self.session)}
        # Force status to 'active' so step 4's update is observable
        session = json.loads(self.session.read_text(encoding='utf-8'))
        session['status'] = 'active'
        self.session.write_text(json.dumps(session, ensure_ascii=False, indent=2),
                                encoding='utf-8')
        # Sentinel content proves step 5 actually rewrites the plan file
        self.plan.write_text('# SENTINEL — should be replaced by wrapup\n',
                             encoding='utf-8')

    def tearDown(self):
        for path, data in self.backups.items():
            helpers.restore_file(path, data)

    def _run_wrapup(self):
        ex = ProtocolExecutor()
        ok = ex.execute('wrapup')
        return ok, ex

    def test_wrapup_all_steps_succeed(self):
        ok, ex = self._run_wrapup()
        self.assertTrue(ok, f'wrapup failed: {ex.state}')
        self.assertEqual(len(ex.state), 5)
        for sid, r in ex.state.items():
            self.assertTrue(r.get('success'), f'step {sid} failed: {r}')
        # Step 4 (call_manager update) must report a truthy write result
        step4 = ex.state[4]['result']
        self.assertTrue(step4, f'step 4 update returned: {step4!r}')

    def test_session_status_flipped_to_ended(self):
        ok, _ = self._run_wrapup()
        self.assertTrue(ok)
        session = json.loads(self.session.read_text(encoding='utf-8'))
        self.assertEqual(session['status'], 'ended')
        # Merge semantics: other keys preserved (full-overwrite would lose them)
        self.assertIn('session_id', session)
        self.assertIn('agent', session)

    def test_hot_md_section_idempotent(self):
        ok, _ = self._run_wrapup()
        self.assertTrue(ok)
        content = self.hot.read_text(encoding='utf-8')
        self.assertEqual(content.count('## 最近会话'), 1)
        # Second run: still exactly one section
        ok2, _ = self._run_wrapup()
        self.assertTrue(ok2)
        content2 = self.hot.read_text(encoding='utf-8')
        self.assertEqual(content2.count('## 最近会话'), 1)
        self.assertIn('- 会话:', content2)

    def test_log_md_appends_one_line_per_run(self):
        before = len(self.log.read_text(encoding='utf-8').splitlines())
        ok, _ = self._run_wrapup()
        self.assertTrue(ok)
        after = len(self.log.read_text(encoding='utf-8').splitlines())
        self.assertEqual(after, before + 1)

    def test_next_plan_rewritten(self):
        ok, _ = self._run_wrapup()
        self.assertTrue(ok)
        after = self.plan.read_text(encoding='utf-8')
        self.assertNotIn('SENTINEL', after, 'next-plan file was not rewritten')
        self.assertIn('# 下次工作计划', after)
        self.assertIn('## 下次进站操作', after)
        # Content is regenerated from current state
        self.assertIn('- 会话:', after)


if __name__ == '__main__':
    unittest.main()

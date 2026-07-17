# -*- coding: utf-8 -*-
"""Executor 'check' protocol test.

Writes only to reports/ (gitignored runtime output).
"""

import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import helpers  # noqa: F401  (sys.path bootstrap)

from executor import ProtocolExecutor


class TestExecutorCheck(unittest.TestCase):
    def test_check_protocol(self):
        ex = ProtocolExecutor()
        ok = ex.execute('check')
        self.assertTrue(ok, 'check protocol should complete')
        # All 5 steps succeeded
        self.assertEqual(len(ex.state), 5)
        for sid, r in ex.state.items():
            self.assertTrue(r.get('success'), f'step {sid} failed: {r}')
        # check_links step returns structured result
        self.assertIn('broken_count', ex.state[4]['result'])
        # Report file: {date} placeholder resolved to today
        report = helpers.BASE_DIR / 'reports' / f'check-{date.today().isoformat()}.md'
        self.assertTrue(report.exists(), f'missing report: {report}')
        self.assertNotIn('{date}', report.name)
        content = report.read_text(encoding='utf-8')
        self.assertIn('# Report', content)
        # Report must contain actual findings, not just step statuses
        self.assertIn('## Step 4', content)
        self.assertIn('broken_count', content)


if __name__ == '__main__':
    unittest.main()

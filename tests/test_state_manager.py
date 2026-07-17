# -*- coding: utf-8 -*-
"""StateManager tests: lock, validate, merge, history, recover.

Uses a temporary state_dir per test — never touches the real state/.
"""

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import helpers  # noqa: F401  (sys.path bootstrap)

from manager import StateManager


class TestStateManager(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix='sm-test-'))
        self.sm = StateManager(state_dir=self.tmp)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    # --- lock ---

    def test_lock_acquire_and_release(self):
        token = self.sm.acquire('session.json', 'agent-a')
        self.assertIsNotNone(token)
        self.assertTrue(self.sm.release('session.json', token))

    def test_lock_double_acquire_fails(self):
        token = self.sm.acquire('session.json', 'agent-a')
        self.assertIsNotNone(token)
        # Second acquire must time out quickly (lock held, not stale)
        token2 = self.sm.acquire('session.json', 'agent-b', timeout_s=1)
        self.assertIsNone(token2)
        self.assertTrue(self.sm.release('session.json', token))
        # After release, acquire succeeds again
        token3 = self.sm.acquire('session.json', 'agent-b', timeout_s=1)
        self.assertIsNotNone(token3)
        self.sm.release('session.json', token3)

    def test_release_with_wrong_token_fails(self):
        token = self.sm.acquire('session.json', 'agent-a')
        self.assertIsNotNone(token)
        self.assertFalse(self.sm.release('session.json', 'forged-token'))
        self.sm.release('session.json', token)

    # --- validate ---

    def test_validate_rejects_missing_keys(self):
        # session.json requires session_id/status/agent
        ok = self.sm.write('session.json', {'session_id': 's1'}, 'agent-a')
        self.assertFalse(ok)
        self.assertIsNone(self.sm.read('session.json'))

    def test_validate_accepts_complete_keys(self):
        ok = self.sm.write('session.json',
                           {'session_id': 's1', 'status': 'active', 'agent': 'a'},
                           'agent-a')
        self.assertTrue(ok)

    # --- merge / optimistic concurrency ---

    def test_merge_version_conflict(self):
        r1 = self.sm.merge('task-queue.json', {'tasks': []}, 'agent-a')
        self.assertTrue(r1['success'])
        self.assertEqual(r1['new_version'], 1)
        # Stale base_version -> conflict
        r2 = self.sm.merge('task-queue.json', {'tasks': [1]}, 'agent-b',
                           base_version=99)
        self.assertFalse(r2['success'])
        self.assertTrue(r2['conflict'])
        # Correct base_version -> success
        r3 = self.sm.merge('task-queue.json', {'tasks': [1]}, 'agent-b',
                           base_version=1)
        self.assertTrue(r3['success'])
        self.assertEqual(r3['new_version'], 2)

    # --- history / recover ---

    def test_write_generates_history(self):
        data = {'tasks': []}
        self.assertTrue(self.sm.write('task-queue.json', data, 'agent-a'))
        self.assertTrue(self.sm.write('task-queue.json', {'tasks': ['t1']}, 'agent-a'))
        history = self.sm.get_history('task-queue.json')
        self.assertGreaterEqual(len(history), 1)
        self.assertEqual(history[-1]['data'], data)

    def test_recover_rolls_back_to_previous_version(self):
        v1 = {'session_id': 's1', 'status': 'active', 'agent': 'a'}
        v2 = {'session_id': 's1', 'status': 'ended', 'agent': 'a'}
        self.assertTrue(self.sm.write('session.json', v1, 'agent-a'))
        self.assertTrue(self.sm.write('session.json', v2, 'agent-a'))
        self.assertEqual(self.sm.read('session.json')['status'], 'ended')
        self.assertTrue(self.sm.recover('session.json'))
        self.assertEqual(self.sm.read('session.json'), v1)


if __name__ == '__main__':
    unittest.main()

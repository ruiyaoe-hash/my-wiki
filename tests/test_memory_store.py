# -*- coding: utf-8 -*-
"""MemoryStore tests: L0 working memory, L1 session records, query filters,
record_type regression, archive_task.

Internal paths (_session_dir / _project_file) are redirected to a temp dir
after construction — the real memory/ store is never written.
"""

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import helpers  # noqa: F401  (sys.path bootstrap)

from memory_store import MemoryStore


class TestMemoryStore(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix='ms-test-'))
        self.ms = MemoryStore()
        self.ms._session_dir = self.tmp / 'sessions'
        self.ms._session_dir.mkdir(parents=True, exist_ok=True)
        self.ms._project_file = self.tmp / 'project.json'
        self.ms._init_project()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    # --- L0: working memory ---

    def test_l0_set_get_clear(self):
        self.ms.wm_set('key', {'a': 1})
        self.assertEqual(self.ms.wm_get('key'), {'a': 1})
        self.assertEqual(self.ms.wm_get('missing', 'default'), 'default')
        self.ms.wm_clear()
        self.assertIsNone(self.ms.wm_get('key'))

    # --- L1: session memory ---

    def test_session_write_and_read(self):
        self.ms.write('session', 'test-s1', 'first note')
        self.ms.write('session', 'test-s1', 'second note')
        records = self.ms.read('session', 'test-s1')
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0]['content'], 'first note')
        self.assertEqual(records[1]['content'], 'second note')

    def test_query_filters_by_record_type(self):
        self.ms.write('session', 'test-s1', 'a note', record_type='note')
        self.ms.write('session', 'test-s1', 'a decision', record_type='decision')
        notes = self.ms.query('session', 'test-s1', record_type='note')
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0]['content'], 'a note')
        everything = self.ms.query('session', 'test-s1')
        self.assertEqual(len(everything), 2)

    def test_record_type_milestone_regression(self):
        """Regression: record_type='milestone' must round-trip as 'milestone'
        (a previous bug dropped the caller-supplied record_type)."""
        self.ms.write('session', 'test-s1', 'phase done', record_type='milestone')
        records = self.ms.read('session', 'test-s1')
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]['type'], 'milestone')

    # --- archive_task ---

    def test_archive_task_creates_task_archive_record(self):
        task_state = {
            'task_id': 'task-001',
            'status': 'completed',
            'context': {'summary': 'did the thing'},
        }
        self.ms.archive_task(task_state, 'test-s1')
        archives = self.ms.query('session', 'test-s1', record_type='task_archive')
        self.assertEqual(len(archives), 1)
        self.assertIn('task-001', archives[0]['content'])
        self.assertEqual(archives[0]['metadata']['status'], 'completed')

    # --- L2: project memory (smoke) ---

    def test_project_write_and_query(self):
        self.ms.write('project', 'decisions', 'use stdlib only', record_type='decision')
        decisions = self.ms.query('project', 'decisions', record_type='decision')
        self.assertEqual(len(decisions), 1)
        self.assertEqual(decisions[0]['content'], 'use stdlib only')


if __name__ == '__main__':
    unittest.main()

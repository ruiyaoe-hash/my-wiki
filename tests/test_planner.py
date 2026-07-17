# -*- coding: utf-8 -*-
"""Planner end-to-end test: enqueue -> run_loop -> archive.

Backs up state/task-queue.json, state/current-task.json, state/session.json
and restores them afterwards; the test session archive under
memory/sessions/ is removed (or restored if it pre-existed).
"""

import json
import sys
import unittest
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import helpers

from planner import Planner

BASE = helpers.BASE_DIR
TASK_ID = 'test-planner-check-001'


class TestPlanner(unittest.TestCase):
    def setUp(self):
        self.queue_file = BASE / 'state' / 'task-queue.json'
        self.current_file = BASE / 'state' / 'current-task.json'
        self.session_file = BASE / 'state' / 'session.json'
        self.backups = {p: helpers.backup_file(p) for p in
                        (self.queue_file, self.current_file, self.session_file)}
        # Use an isolated test session id so the archive never collides
        # with archives left by real runtime runs (which reuse session.json)
        test_session_id = f'test-planner-{uuid.uuid4().hex[:8]}'
        self.session_file.write_text(json.dumps({
            'session_id': test_session_id, 'status': 'active', 'agent': 'TestPlanner'
        }, ensure_ascii=False, indent=2), encoding='utf-8')
        self.session_archive = BASE / 'memory' / 'sessions' / f'{test_session_id}.json'
        self.archive_backup = helpers.backup_file(self.session_archive)
        # Enqueue one check task via merge (validates + version-bumps)
        self.planner = Planner()
        result = self.planner.sm.merge('task-queue.json', {
            'tasks': [{
                'task_id': TASK_ID,
                'task_type': 'check',
                'priority': 1,
                'description': 'planner integration test',
                'context': {'scope': 'knowledge', 'summary': 'planner test run'},
            }]
        }, 'TestPlanner')
        if not result.get('success'):
            self.fail(f'could not enqueue test task: {result}')

    def tearDown(self):
        for path, data in self.backups.items():
            helpers.restore_file(path, data)
        helpers.restore_file(self.session_archive, self.archive_backup)

    def test_run_loop_processes_one_task(self):
        completed = self.planner.run_loop(max_tasks=1)
        self.assertEqual(completed, 1)

        # current-task.json marked completed
        ct = json.loads(self.current_file.read_text(encoding='utf-8'))
        self.assertEqual(ct['task_id'], TASK_ID)
        self.assertEqual(ct['status'], 'completed')
        self.assertEqual(ct['progress'], 1.0)

        # queue drained
        queue = json.loads(self.queue_file.read_text(encoding='utf-8'))
        self.assertEqual(queue['tasks'], [])

        # session archive contains the task_archive record
        self.assertTrue(self.session_archive.exists(),
                        f'missing session archive: {self.session_archive}')
        archive = json.loads(self.session_archive.read_text(encoding='utf-8'))
        task_records = [r for r in archive.get('records', [])
                        if r.get('type') == 'task_archive']
        self.assertEqual(len(task_records), 1)
        self.assertIn(TASK_ID, task_records[0]['content'])


if __name__ == '__main__':
    unittest.main()

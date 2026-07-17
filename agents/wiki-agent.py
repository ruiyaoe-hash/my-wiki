# -*- coding: utf-8 -*-
"""Wiki Maintenance Agent v0.1 — first Application.

Thin wrapper around Planner. Has two core behaviors:
1. check: lint the wiki (stale pages, broken links)
2. run: process the task queue end-to-end
"""

import sys, os
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / 'planner'))

from planner import Planner


class WikiAgent:
    """Minimal wiki maintenance agent."""

    def __init__(self):
        self.planner = Planner()

    def check(self):
        """Run a quick check protocol (single task)."""
        # Enqueue a check task
        self.planner.sm.merge('task-queue.json', {
            'tasks': [{
                'task_id': 'wiki-check-001',
                'task_type': 'check',
                'priority': 1,
                'description': 'Wiki lint check: stale pages and broken links',
                'created_at': '2026-07-17T03:00:00Z',
                'context': {'scope': 'knowledge'}
            }]
        }, 'WikiAgent')

        # Run one iteration
        completed = self.planner.run_loop(max_tasks=1)
        print(f'WikiAgent check: {completed} task(s) completed')
        return self.planner.status()

    def status(self):
        """Return agent status overview."""
        return self.planner.status()


if __name__ == '__main__':
    agent = WikiAgent()
    print('=== WikiAgent Check ===')
    result = agent.check()
    print(f'Status: {result}')
    print('Done.')

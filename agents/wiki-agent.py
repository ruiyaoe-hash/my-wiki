# -*- coding: utf-8 -*-
"""Wiki Maintenance Agent v0.2 — first Application.

Thin wrapper around Planner. Has two core behaviors:
1. check: lint the wiki (stale pages, broken links)
2. run: process the task queue end-to-end

CLI:
    python agents/wiki-agent.py [--loop N] [--interval S] [--recover]

--loop N      run N rounds (default 1); each round enqueues one check task
              and processes it via run_loop(max_tasks=1)
--interval S  seconds to sleep between rounds (default 0)
--recover     on startup, if state/current-task.json is left in 'running'
              status (i.e. the previous run was killed), roll it back via
              StateManager.recover and print the recovery info
"""

import argparse
import sys, os, time
from datetime import datetime
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

    def recover_if_interrupted(self):
        """If current-task.json says 'running' (previous run was killed),
        roll back to the last consistent state and report. Returns True if
        a recovery happened."""
        task = self.planner.sm.read('current-task.json') or {}
        if task.get('status') != 'running':
            return False
        task_id = task.get('task_id')
        ok = self.planner.sm.recover('current-task.json')
        restored = self.planner.sm.read('current-task.json') or {}
        if ok:
            print(f'[recover] 检测到被中断的任务 {task_id}（status=running），'
                  f'已从历史恢复: status={restored.get("status")}, '
                  f'task_id={restored.get("task_id")}')
        else:
            print(f'[recover] 检测到被中断的任务 {task_id}（status=running），'
                  f'但无历史可恢复')
        return ok

    def run(self, loop=1, interval=0):
        """Run `loop` rounds; each round enqueues one check task and runs it."""
        run_id = 'wiki-' + datetime.now().strftime('%Y-%m-%d-%H%M%S')
        total = 0
        for i in range(loop):
            session_id = f'{run_id}-{i + 1:02d}'
            task_id = f'{run_id}-check-{i + 1:02d}'
            self.planner.sm.merge('task-queue.json', {
                'tasks': [{
                    'task_id': task_id,
                    'task_type': 'check',
                    'priority': 1,
                    'description': 'Wiki lint check: stale pages and broken links',
                    'created_at': datetime.now().isoformat(),
                    'context': {'scope': 'knowledge',
                                'summary': f'wiki-agent 例行检查 第 {i + 1} 轮'},
                }]
            }, 'WikiAgent')
            completed = self.planner.run_loop(max_tasks=1, session_id=session_id)
            total += completed
            print(f'[round {i + 1}/{loop}] session={session_id} '
                  f'completed={completed}')
            if interval and i < loop - 1:
                time.sleep(interval)
        print(f'WikiAgent run: {total}/{loop} task(s) completed')
        return total


def main(argv=None):
    parser = argparse.ArgumentParser(description='Wiki Maintenance Agent')
    parser.add_argument('--loop', type=int, default=1,
                        help='number of rounds to run (default 1)')
    parser.add_argument('--interval', type=float, default=0,
                        help='seconds to sleep between rounds (default 0)')
    parser.add_argument('--recover', action='store_true',
                        help="recover a killed run (current-task stuck at 'running')")
    args = parser.parse_args(argv)

    agent = WikiAgent()
    if args.recover:
        agent.recover_if_interrupted()
    agent.run(loop=args.loop, interval=args.interval)
    print('Done.')


if __name__ == '__main__':
    main()

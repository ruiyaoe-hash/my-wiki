# -*- coding: utf-8 -*-
"""Planner v0.1 — dynamic orchestration engine.

Responsibilities:
1. Read task-queue, pick next task, match to protocol
2. Execute protocol steps via ProtocolExecutor
3. Emit Events on state changes
4. Archive completed tasks to Memory Store
"""

import sys, os, json
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / 'state_manager'))
sys.path.insert(0, str(BASE / 'executor'))
sys.path.insert(0, str(BASE / 'event_bus'))
sys.path.insert(0, str(BASE / 'memory'))

from manager import StateManager
from executor import ProtocolExecutor
from event_bus import get_bus, Event, EventTypes
from memory_store import MemoryStore


# Protocol matching table
TASK_TYPE_TO_PROTOCOL = {
    'check': 'check',
    'ingest': 'ingest',
    'wrapup': 'wrapup',
    'review': 'check',       # fallback to check
    'build': 'check',        # fallback
}


class Planner:
    """The central execution loop. Picks tasks, runs protocols, records results."""

    def __init__(self):
        self.sm = StateManager()
        self.executor = ProtocolExecutor()
        self.bus = get_bus()
        self.memory = MemoryStore()
        self.current_session = None

    def _update_execution_status(self, **fields):
        """Merge-update state/execution-status.json, preserving counters."""
        current = self.sm.read('execution-status.json') or {}
        updates = {
            'status': current.get('status', 'idle'),
            'last_run': current.get('last_run'),
            'tasks_processed': current.get('tasks_processed', 0),
            'sessions_total': current.get('sessions_total', 0),
        }
        updates.update(fields)
        if updates['last_run'] is None:
            updates['last_run'] = datetime.now(timezone.utc).isoformat()
        return self.sm.merge('execution-status.json', updates, 'Planner')

    def start_session(self, session_id=None):
        """Start a new session."""
        session = self.sm.read('session.json') or {}
        session['session_id'] = session_id or session.get('session_id', 'auto-generated')
        session['status'] = 'active'
        self.sm.write('session.json', session, 'Planner')
        self.current_session = session['session_id']

        self._update_execution_status(
            status='active', last_run=datetime.now(timezone.utc).isoformat())

        self.bus.emit(Event(EventTypes.SESSION_STARTED,
                           {'session_id': self.current_session}, source='Planner'))
        return self.current_session

    def end_session(self, tasks_completed=0):
        """End current session and archive all tasks."""
        session = self.sm.read('session.json')
        if session:
            session['status'] = 'ended'
            self.sm.write('session.json', session, 'Planner')

        task = self.sm.read('current-task.json')
        if task and task.get('task_id'):
            self.memory.archive_task(task, self.current_session)

        current = self.sm.read('execution-status.json') or {}
        self._update_execution_status(
            status='idle',
            tasks_processed=current.get('tasks_processed', 0) + tasks_completed,
            sessions_total=current.get('sessions_total', 0) + 1)

        self.bus.emit(Event(EventTypes.SESSION_ENDED,
                           {'session_id': self.current_session}, source='Planner'))

        # Clear working memory
        self.memory.wm_clear()
        return self.current_session

    def execute_next_task(self):
        """Pick next task from queue and execute it."""
        queue = self.sm.read('task-queue.json')
        if not queue or not queue.get('tasks'):
            return None

        next_task = queue['tasks'].pop(0)
        self.sm.write('task-queue.json', queue, 'Planner')

        self.sm.write('current-task.json', {
            'task_id': next_task.get('task_id', 'auto'),
            'task_type': next_task.get('task_type', 'check'),
            'status': 'running',
            'current_step': 0,
            'total_steps': 5,
            'progress': 0.0,
            'owner_agent': 'Planner',
            'context': next_task
        }, 'Planner')

        self.bus.emit(Event(EventTypes.TASK_STARTED,
                           {'task_id': next_task.get('task_id'), 'type': next_task.get('task_type')},
                           source='Planner'))

        return next_task

    def run_task(self, task):
        """Execute a single task."""
        task_type = task.get('task_type', 'check')
        protocol_id = TASK_TYPE_TO_PROTOCOL.get(task_type, 'check')

        self.bus.emit(Event(EventTypes.PROTOCOL_STARTED,
                           {'protocol': protocol_id, 'task_id': task.get('task_id')},
                           source='Planner'))

        try:
            ok = self.executor.execute(protocol_id, inputs=task.get('context', {}))
        except Exception as e:
            ok = False
            self.bus.emit(Event(EventTypes.AGENT_ERROR, {'error': str(e), 'task': task}, source='Planner'))

        if ok:
            self.bus.emit(Event(EventTypes.TASK_COMPLETED,
                               {'task_id': task.get('task_id')}, source='Planner'))
            # Update current-task to completed
            ct = self.sm.read('current-task.json')
            ct['status'] = 'completed'
            ct['progress'] = 1.0
            self.sm.write('current-task.json', ct, 'Planner')
        else:
            self.bus.emit(Event(EventTypes.TASK_FAILED,
                               {'task_id': task.get('task_id')}, source='Planner'))
            ct = self.sm.read('current-task.json')
            ct['status'] = 'failed'
            self.sm.write('current-task.json', ct, 'Planner')

        self.bus.emit(Event(EventTypes.PROTOCOL_COMPLETED,
                           {'protocol': protocol_id, 'success': ok}, source='Planner'))
        return ok

    def run_loop(self, max_tasks=5, session_id=None):
        """Main loop: process up to max_tasks from queue."""
        self.start_session(session_id=session_id)
        completed = 0
        for _ in range(max_tasks):
            task = self.execute_next_task()
            if not task:
                break
            if self.run_task(task):
                completed += 1
        self.end_session(tasks_completed=completed)

        # Persist event history
        self.bus.persist()
        return completed

    def status(self):
        """Return current planner state overview."""
        queue = self.sm.read('task-queue.json')
        ct = self.sm.read('current-task.json')
        return {
            'queue_size': len(queue.get('tasks', [])) if queue else 0,
            'current_task': ct.get('task_id') if ct else None,
            'current_status': ct.get('status') if ct else None,
            'event_history': len(self.bus.get_history()),
            'memory': self.memory.status()
        }

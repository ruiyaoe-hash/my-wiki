# -*- coding: utf-8 -*-
"""Event Bus v0.1 — pub/sub for Agent Runtime.

Events are typed, immutable, fire-and-forget. Subscribers register by event_type.
Phase 1: stub interface. Phase 3: full implementation with history.
"""

import json, os, uuid
from datetime import datetime, timezone
from pathlib import Path

HISTORY_DIR = Path(__file__).resolve().parent / 'history'
HISTORY_DIR.mkdir(parents=True, exist_ok=True)


class Event:
    """An immutable event emitted by a component."""

    def __init__(self, event_type, payload, source='unknown'):
        self.id = str(uuid.uuid4())[:8]
        self.type = event_type
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.payload = payload or {}
        self.source = source

    def to_dict(self):
        return {
            'id': self.id, 'type': self.type,
            'timestamp': self.timestamp,
            'payload': self.payload, 'source': self.source
        }

    def __repr__(self):
        return f'Event({self.type}, {self.id})'


class EventBus:
    """Central pub/sub event bus.

    Usage:
        bus = EventBus()
        bus.subscribe('task.created', my_handler)
        bus.emit(Event('task.created', {'task_id': '...'}))
    """

    def __init__(self):
        self._subscribers = {}   # event_type -> [handler]
        self._history = []       # all emitted events
        self._persisted_counts = {}  # resolved filepath -> # events already written

    def subscribe(self, event_type, handler):
        """Register a handler for an event type. Handler receives Event object."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)
        return self

    def unsubscribe(self, event_type, handler):
        """Remove a specific handler."""
        if event_type in self._subscribers:
            self._subscribers[event_type] = [h for h in self._subscribers[event_type] if h != handler]

    def emit(self, event):
        """Emit an event to all subscribers of its type."""
        self._history.append(event)
        handlers = self._subscribers.get(event.type, [])
        results = []
        for handler in handlers:
            try:
                results.append(handler(event))
            except Exception as e:
                results.append({'error': str(e)})
        return results

    def get_history(self, event_type=None, limit=50):
        """Get recent events, optionally filtered by type."""
        events = self._history
        if event_type:
            events = [e for e in events if e.type == event_type]
        return [e.to_dict() for e in events[-limit:]]

    def persist(self, filepath=None):
        """Append new events to the jsonl history file.

        Only events emitted since the last persist() to the same file are
        written, so repeated calls never duplicate lines. Returns the path.
        """
        path = Path(filepath) if filepath else HISTORY_DIR / 'events.jsonl'
        key = str(path.resolve())
        start = self._persisted_counts.get(key, 0)
        new_events = self._history[start:]
        if new_events:
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'a', encoding='utf-8') as f:
                for event in new_events:
                    f.write(json.dumps(event.to_dict(), ensure_ascii=False) + '\n')
        self._persisted_counts[key] = len(self._history)
        return str(path)

    def load_history(self, filepath=None):
        """Read events back from a jsonl history file (offline queries).

        Returns a list of event dicts; missing file -> empty list.
        Blank or malformed lines are skipped.
        """
        path = Path(filepath) if filepath else HISTORY_DIR / 'events.jsonl'
        if not path.exists():
            return []
        events = []
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        return events

    def clear(self):
        """Clear all subscribers and history."""
        self._subscribers.clear()
        self._history.clear()
        self._persisted_counts.clear()


# Singleton for the whole Runtime
_instance = None

def get_bus():
    """Get the singleton EventBus instance."""
    global _instance
    if _instance is None:
        _instance = EventBus()
    return _instance


# --- Standard event types ---
class EventTypes:
    TASK_CREATED = 'task.created'
    TASK_STARTED = 'task.started'
    TASK_STEP_COMPLETED = 'task.step_completed'
    TASK_COMPLETED = 'task.completed'
    TASK_FAILED = 'task.failed'
    
    STATE_UPDATED = 'state.updated'
    SESSION_STARTED = 'session.started'
    SESSION_ENDED = 'session.ended'
    
    KNOWLEDGE_CREATED = 'knowledge.created'
    KNOWLEDGE_UPDATED = 'knowledge.updated'
    KNOWLEDGE_STALE = 'knowledge.stale'
    
    PROTOCOL_STARTED = 'protocol.started'
    PROTOCOL_STEP_DONE = 'protocol.step_done'
    PROTOCOL_COMPLETED = 'protocol.completed'
    
    AGENT_ERROR = 'agent.error'
    EVR_EXTRACTION = 'evr.extraction'

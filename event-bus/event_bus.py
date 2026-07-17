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
        """Save event history to disk."""
        path = Path(filepath) if filepath else HISTORY_DIR / 'events.jsonl'
        with open(path, 'w', encoding='utf-8') as f:
            for event in self._history:
                f.write(json.dumps(event.to_dict(), ensure_ascii=False) + '\n')
        return str(path)

    def clear(self):
        """Clear all subscribers and history."""
        self._subscribers.clear()
        self._history.clear()


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

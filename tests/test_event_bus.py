# -*- coding: utf-8 -*-
"""EventBus tests: pub/sub, exception isolation, unsubscribe, persist."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import helpers  # noqa: F401  (sys.path bootstrap)

from event_bus import Event, EventBus


class TestEventBus(unittest.TestCase):
    def setUp(self):
        # Fresh instance per test — never the process-wide singleton
        self.bus = EventBus()

    def test_emit_reaches_subscriber(self):
        received = []
        self.bus.subscribe('test.event', received.append)
        ev = Event('test.event', {'k': 'v'}, source='test')
        results = self.bus.emit(ev)
        self.assertEqual(len(received), 1)
        self.assertIs(received[0], ev)
        self.assertEqual(len(results), 1)

    def test_subscriber_exception_isolated(self):
        calls = []

        def bad_handler(event):
            raise RuntimeError('boom')

        def good_handler(event):
            calls.append(event)
            return 'ok'

        self.bus.subscribe('test.event', bad_handler)
        self.bus.subscribe('test.event', good_handler)
        results = self.bus.emit(Event('test.event', {}))
        # Good handler still ran despite the bad one raising
        self.assertEqual(len(calls), 1)
        # Bad handler's exception captured as error dict, not raised
        self.assertEqual(len(results), 2)
        self.assertIn('error', results[0])
        self.assertEqual(results[1], 'ok')

    def test_unsubscribe(self):
        received = []

        def handler(event):
            received.append(event)

        self.bus.subscribe('test.event', handler)
        self.bus.emit(Event('test.event', {}))
        self.assertEqual(len(received), 1)
        self.bus.unsubscribe('test.event', handler)
        self.bus.emit(Event('test.event', {}))
        self.assertEqual(len(received), 1)

    def test_persist_writes_parseable_jsonl(self):
        self.bus.emit(Event('test.a', {'n': 1}))
        self.bus.emit(Event('test.b', {'n': 2}))
        with tempfile.TemporaryDirectory(prefix='eb-test-') as tmp:
            out = Path(tmp) / 'events.jsonl'
            path = self.bus.persist(str(out))
            self.assertEqual(Path(path), out)
            lines = out.read_text(encoding='utf-8').strip().splitlines()
            self.assertEqual(len(lines), 2)
            records = [json.loads(line) for line in lines]
            self.assertEqual(records[0]['type'], 'test.a')
            self.assertEqual(records[1]['payload'], {'n': 2})
            for r in records:
                self.assertIn('id', r)
                self.assertIn('timestamp', r)


if __name__ == '__main__':
    unittest.main()

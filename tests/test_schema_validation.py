# -*- coding: utf-8 -*-
"""Knowledge sidecar schema validation (stdlib-only, hand-rolled).

Every knowledge/*.json sidecar (except metadata-schema.json itself) must
carry the required keys, and type/domain/status values must fall inside
the enums declared in knowledge/metadata-schema.json.
"""

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import helpers  # noqa: F401  (sys.path bootstrap)

KNOWLEDGE_DIR = helpers.BASE_DIR / 'knowledge'

REQUIRED_KEYS = [
    'knowledge_id', 'title', 'path', 'created', 'updated',
    'type', 'domain', 'status', 'tags', 'outgoing_links', 'freshness_score',
]
ENUM_FIELDS = ['type', 'domain', 'status']


class TestSchemaValidation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        schema_path = KNOWLEDGE_DIR / 'metadata-schema.json'
        cls.schema = json.loads(schema_path.read_text(encoding='utf-8'))
        cls.enums = {
            field: set(cls.schema['properties'][field]['enum'])
            for field in ENUM_FIELDS
        }
        cls.sidecars = sorted(
            p for p in KNOWLEDGE_DIR.glob('*.json')
            if p.name != 'metadata-schema.json'
        )
        if not cls.sidecars:
            # Fresh clone / CI: personal content is gitignored, so no sidecars.
            raise unittest.SkipTest(
                'no knowledge sidecars in this checkout '
                '(regenerate with scripts/rebuild_sidecars.py)')

    def test_sidecars_exist(self):
        self.assertGreater(len(self.sidecars), 0, 'no sidecars found')

    def test_required_keys_present(self):
        problems = []
        for path in self.sidecars:
            try:
                sc = json.loads(path.read_text(encoding='utf-8'))
            except json.JSONDecodeError as e:
                problems.append(f'{path.name}: invalid JSON: {e}')
                continue
            missing = [k for k in REQUIRED_KEYS if k not in sc]
            if missing:
                problems.append(f'{path.name}: missing keys {missing}')
        self.assertEqual(problems, [],
                         f'{len(problems)} sidecar(s) with problems:\n'
                         + '\n'.join(problems[:50]))

    def test_enum_values_valid(self):
        problems = []
        for path in self.sidecars:
            try:
                sc = json.loads(path.read_text(encoding='utf-8'))
            except json.JSONDecodeError:
                continue  # reported by the other test
            for field in ENUM_FIELDS:
                value = sc.get(field)
                if value is None:
                    continue  # missing key reported by the other test
                if value not in self.enums[field]:
                    problems.append(
                        f'{path.name}: {field}={value!r} not in '
                        f'{sorted(self.enums[field], key=repr)}')
        self.assertEqual(problems, [],
                         f'{len(problems)} enum violation(s):\n'
                         + '\n'.join(problems[:50]))


if __name__ == '__main__':
    unittest.main()

# -*- coding: utf-8 -*-
"""Memory Store v0.2 — full L0-L4 of the five-layer memory architecture.

L0: Working Memory  — in-memory dict, evicted on Task completion
L1: Session Memory  — persisted JSON per session
L2: Project Memory  — persistent project-wide records
L3: Semantic Memory — knowledge page index (sem_index / sem_search)
L4: Archive         — sessions older than N days moved to archive/

Five-verb protocol: create / read / update / delete / query
Memory records are APPEND-ONLY — never modified, only archived.
"""

import json, os
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MEMORY_DIR = Path(__file__).resolve().parent
MEMORY_DIR.mkdir(parents=True, exist_ok=True)


class MemoryRecord:
    """A single immutable memory entry."""

    def __init__(self, content, record_type='note', source=None, metadata=None):
        self.content = content
        self.type = record_type
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.source = source or 'unknown'
        self.metadata = metadata or {}

    def to_dict(self):
        return {
            'content': self.content,
            'type': self.type,
            'timestamp': self.timestamp,
            'source': self.source,
            'metadata': self.metadata
        }


class MemoryStore:
    """Memory Store implementing L0-L4.

    Usage:
        ms = MemoryStore()
        # Write a session memory
        ms.write('session', '2026-07-17-003', 'Phase 3 started', type='milestone')
        # Read session memory
        ms.read('session', '2026-07-17-003')
        # Query all project records
        ms.query('project', type='decision')
    """

    def __init__(self):
        self.L0 = {}  # Working Memory: key -> Any (volatile)
        self._session_dir = MEMORY_DIR / 'sessions'
        self._session_dir.mkdir(parents=True, exist_ok=True)
        self._project_file = MEMORY_DIR / 'project.json'
        self._init_project()

    # --- L0: Working Memory (volatile) ---

    def wm_set(self, key, value):
        """Set a working memory value. Volatile."""
        self.L0[key] = value

    def wm_get(self, key, default=None):
        """Get a working memory value."""
        return self.L0.get(key, default)

    def wm_clear(self):
        """Clear working memory (called on Task completion)."""
        self.L0.clear()

    # --- L1: Session Memory (persisted) ---

    def _init_project(self):
        """Initialize project memory file if not exists."""
        if not self._project_file.exists():
            self._project_file.write_text(json.dumps({'records': [], 'decisions': [], 'milestones': []},
                                                     ensure_ascii=False, indent=2), encoding='utf-8')

    def _load_session(self, session_id):
        path = self._session_dir / f'{session_id}.json'
        if path.exists():
            return json.loads(path.read_text(encoding='utf-8'))
        return {'session_id': session_id, 'records': [], 'started_at': datetime.now(timezone.utc).isoformat()}

    def _save_session(self, session_id, data):
        path = self._session_dir / f'{session_id}.json'
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

    def write(self, level, scope, content, **kwargs):
        """Write a memory record to L1 (session) or L2 (project).

        level: 'session' or 'project'
        scope: session_id (for session) or category (for project: 'decisions', 'milestones', 'records')
        """
        record = MemoryRecord(content, record_type=kwargs.get('record_type', 'note'),
                              source=kwargs.get('source'), metadata=kwargs.get('metadata', {}))

        if level == 'session':
            data = self._load_session(scope)
            data['records'].append(record.to_dict())
            self._save_session(scope, data)
            return record

        elif level == 'project':
            proj = json.loads(self._project_file.read_text(encoding='utf-8'))
            if scope not in proj:
                proj[scope] = []
            proj[scope].append(record.to_dict())
            self._project_file.write_text(json.dumps(proj, ensure_ascii=False, indent=2), encoding='utf-8')
            return record

        else:
            raise ValueError(f'Unknown memory level: {level}')

    def read(self, level, scope, limit=None):
        """Read memory records."""
        if level == 'session':
            data = self._load_session(scope)
            records = data.get('records', [])
        elif level == 'project':
            proj = json.loads(self._project_file.read_text(encoding='utf-8'))
            records = proj.get(scope, [])
        else:
            raise ValueError(f'Unknown memory level: {level}')

        if limit:
            records = records[-limit:]
        return records

    def query(self, level, scope=None, record_type=None, source=None):
        """Query memory records by filters."""
        if level == 'session':
            data = self._load_session(scope) if scope else {}
            records = data.get('records', [])
        elif level == 'project':
            proj = json.loads(self._project_file.read_text(encoding='utf-8'))
            records = []
            if scope:
                records = proj.get(scope, [])
            else:
                for k, v in proj.items():
                    if isinstance(v, list):
                        records.extend(v)
        else:
            records = []

        results = records
        if record_type:
            results = [r for r in results if r.get('type') == record_type]
        if source:
            results = [r for r in results if r.get('source') == source]
        return results

    # --- State integration: archive Task state to Memory ---

    def archive_task(self, task_state, session_id):
        """Archive a completed Task's state as an immutable Memory record."""
        content = f'Task {task_state.get("task_id")} completed: {task_state.get("context", {}).get("summary", "")}'
        return self.write('session', session_id, content, record_type='task_archive',
                         metadata={'task_id': task_state.get('task_id'), 'status': task_state.get('status')})


    # --- L3: Semantic Memory (knowledge page index) ---

    def sem_index(self, force=False):
        """Build or refresh the semantic memory index from all knowledge sidecars."""
        index_path = MEMORY_DIR / 'semantic_index.json'
        if index_path.exists() and not force:
            return json.loads(index_path.read_text(encoding='utf-8'))
        
        kb_dir = BASE_DIR / 'knowledge'
        index = {'pages': {}, 'by_domain': {}, 'by_type': {}, 'total': 0}
        for f in kb_dir.glob('*.json'):
            if f.name == 'metadata-schema.json': continue
            with open(f, 'r', encoding='utf-8') as fp: sc = json.load(fp)
            nid = sc.get('knowledge_id', f.stem)
            index['pages'][nid] = {
                'title': sc.get('title', ''), 'type': sc.get('type', ''),
                'domain': sc.get('domain', ''), 'tags': sc.get('tags', []),
                'status': sc.get('status', ''), 'freshness': sc.get('freshness_score', 0)
            }
            d = sc.get('domain', 'unknown'); index['by_domain'].setdefault(d, []).append(nid)
            t = sc.get('type', 'unknown'); index['by_type'].setdefault(t, []).append(nid)
        index['total'] = len(index['pages'])
        index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding='utf-8')
        return index

    def sem_search(self, query, field='title'):
        """Simple search over semantic memory index."""
        idx = self.sem_index()
        results = []
        for nid, info in idx.get('pages', {}).items():
            if query.lower() in str(info.get(field, '')).lower():
                results.append({**info, 'knowledge_id': nid})
        return results

    # --- L4: Archive ---

    def archive_sessions(self, older_than_days=30):
        """Archive sessions older than N days."""
        from datetime import datetime
        archive_dir = MEMORY_DIR / 'archive'
        archive_dir.mkdir(parents=True, exist_ok=True)
        cutoff = datetime.now().timestamp() - older_than_days * 86400
        moved = 0
        for f in self._session_dir.glob('*.json'):
            if f.stat().st_mtime < cutoff:
                dest = archive_dir / f.name
                f.rename(dest); moved += 1
        return {'archived_sessions': moved}

    def status(self):
        """Return overview of memory store state."""
        sessions = list(self._session_dir.glob('*.json'))
        proj = json.loads(self._project_file.read_text(encoding='utf-8'))
        return {
            'L0_items': len(self.L0),
            'L1_sessions': len(sessions),
            'L2_records': {k: len(v) if isinstance(v, list) else 0 for k, v in proj.items()}
        }

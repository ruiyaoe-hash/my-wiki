# -*- coding: utf-8 -*-
"""Shared test helpers: sys.path bootstrap + file backup/restore utilities.

Every test module inserts tests/ into sys.path and imports this module, so
the runtime components (manager / event_bus / memory_store / executor /
planner) are importable regardless of how unittest is invoked.
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

for _d in ('state_manager', 'event_bus', 'memory', 'executor', 'planner'):
    _p = str(BASE_DIR / _d)
    if _p not in sys.path:
        sys.path.insert(0, _p)


def backup_file(path):
    """Read a file as bytes for later restore. Returns None if missing."""
    path = Path(path)
    if not path.exists():
        return None
    return path.read_bytes()


def restore_file(path, data):
    """Restore bytes previously captured by backup_file.

    data=None means the file did not exist before -> remove it if present.
    """
    path = Path(path)
    if data is None:
        if path.exists():
            path.unlink()
        return
    path.write_bytes(data)

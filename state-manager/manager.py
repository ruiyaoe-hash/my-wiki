# State Manager v0.1
# Thin layer for multi-agent state coordination.
# Responsibilities: lock, validate, read/write, merge, history, recover.

import json, os, time
from datetime import datetime, timezone
from pathlib import Path

STATE_DIR = Path(__file__).resolve().parent.parent / "state"

class StateManager:
    """Coordinates all state file operations with locking and history."""

    def __init__(self, state_dir=None):
        self.state_dir = Path(state_dir) if state_dir else STATE_DIR
        self.lock_dir = self.state_dir / ".locks"
        self.history_dir = self.state_dir / ".history"
        self.lock_dir.mkdir(parents=True, exist_ok=True)
        self.history_dir.mkdir(parents=True, exist_ok=True)

    def acquire(self, filename, agent_id, timeout_s=30):
        """Try to get an optimistic lock. Returns lock token or None."""
        lockfile = self.lock_dir / f"{filename}.lock"
        deadline = time.time() + timeout_s
        while time.time() < deadline:
            try:
                fd = os.open(lockfile, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                token = f"{agent_id}::{datetime.now(timezone.utc).isoformat()}"
                os.write(fd, token.encode("utf-8"))
                os.close(fd)
                return token
            except FileExistsError:
                if self._is_stale(lockfile, 60):
                    os.remove(lockfile)
                    continue
                time.sleep(0.3)
        return None

    def release(self, filename, token):
        lockfile = self.lock_dir / f"{filename}.lock"
        if lockfile.exists():
            try:
                current = lockfile.read_text().strip()
                if current == token:
                    lockfile.unlink()
                    return True
            except Exception:
                pass
        return False

    def _is_stale(self, lockfile, max_age_s):
        try:
            return (time.time() - lockfile.stat().st_mtime) > max_age_s
        except Exception:
            return True

    def read(self, filename):
        filepath = self.state_dir / filename
        if not filepath.exists():
            return None
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def write(self, filename, data, agent_id):
        token = self.acquire(filename, agent_id)
        if not token:
            return False
        try:
            if not self.validate(filename, data):
                return False
            self._save_history(filename)
            filepath = self.state_dir / filename
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        finally:
            self.release(filename, token)

    def validate(self, filename, data):
        # TODO Phase 2: load state-schema.json and validate against it instead of hardcoded rules
        if filename == "current-task.json":
            return all(k in data for k in ["task_id","status","owner_agent"])
        if filename == "task-queue.json":
            return "tasks" in data and isinstance(data["tasks"], list)
        if filename == "session.json":
            return all(k in data for k in ["session_id","status","agent"])
        if filename == "execution-status.json":
            return all(k in data for k in ["status","tasks_processed"])
        return True

    def merge(self, filename, updates, agent_id, base_version=None):
        """Merge updates with optimistic concurrency via _version field.
        Pass base_version to detect conflicts. Returns dict with success/conflict info."""
        current = self.read(filename)
        if current is None:
            current = {}
        if base_version is not None:
            if current.get('_version', 0) != base_version:
                return {
                    'success': False,
                    'conflict': True,
                    'message': f"Version mismatch: current={current.get('_version', 0)}, yours={base_version}",
                    'current_data': current,
                    'your_updates': updates
                }
        new_version = current.get('_version', 0) + 1
        merged = {**current, **updates, '_version': new_version}
        if self.write(filename, merged, agent_id):
            return {'success': True, 'conflict': False, 'new_version': new_version, 'data': merged}
        return {'success': False, 'conflict': False, 'message': 'Write failed'}

    def batch_write(self, file_data_map, agent_id):
        """Atomically write multiple state files. Returns True only if all succeed."""
        locks = {}
        try:
            for filename in file_data_map:
                token = self.acquire(filename, agent_id)
                if not token:
                    for fn, tok in locks.items():
                        self.release(fn, tok)
                    return False
                locks[filename] = token
            for filename, data in file_data_map.items():
                if not self.validate(filename, data):
                    return False
                self._save_history(filename)
                filepath = self.state_dir / filename
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        finally:
            for filename, token in locks.items():
                self.release(filename, token)

    def _save_history(self, filename):
        hist_file = self.history_dir / f"{filename}.history"
        data = self.read(filename)
        if data is None:
            return
        entry = {"timestamp": datetime.now(timezone.utc).isoformat(), "data": data}
        try:
            existing = json.loads(hist_file.read_text(encoding="utf-8")) if hist_file.exists() else []
        except Exception:
            existing = []
        existing.append(entry)
        if len(existing) > 50:
            existing = existing[-50:]
        hist_file.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")

    def get_history(self, filename, limit=10):
        hist_file = self.history_dir / f"{filename}.history"
        if not hist_file.exists():
            return []
        try:
            return json.loads(hist_file.read_text(encoding="utf-8"))[-limit:]
        except Exception:
            return []

    def recover(self, filename):
        history = self.get_history(filename, limit=1)
        if not history:
            return False
        last = history[-1]["data"]
        filepath = self.state_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(last, f, ensure_ascii=False, indent=2)
        return True

    def status(self):
        files = [f for f in os.listdir(self.state_dir) if f.endswith(".json")]
        return {"files": files}

    def health_check(self):
        """Return health status for every state file: readable, locked, history depth."""
        result = {}
        for fn in [f for f in os.listdir(self.state_dir) if f.endswith('.json')]:
            fpath = self.state_dir / fn
            lockfile = self.lock_dir / f'{fn}.lock'
            hist_file = self.history_dir / f'{fn}.history'
            info = {'readable': False, 'locked': False, 'history_depth': 0}
            try:
                with open(fpath, 'r', encoding='utf-8') as f:
                    json.load(f)
                info['readable'] = True
            except Exception:
                pass
            info['locked'] = lockfile.exists()
            if hist_file.exists():
                try:
                    info['history_depth'] = len(json.loads(hist_file.read_text(encoding='utf-8')))
                except Exception:
                    pass
            result[fn] = info
        return result

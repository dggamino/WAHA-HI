"""
Persistent Context Memory Foundation v0.1.0
"""

import json
from pathlib import Path
from datetime import datetime


class MemoryStore:

    def __init__(self, path="data/memory.json"):

        self.path = Path(path)

        self.path.parent.mkdir(
            exist_ok=True
        )

        if not self.path.exists():
            self.path.write_text("{}")


    def _read(self):

        return json.loads(
            self.path.read_text()
        )


    def _write(self, data):

        self.path.write_text(
            json.dumps(
                data,
                indent=2,
                ensure_ascii=False
            )
        )


    def save(self, session_id, data):

        storage = self._read()

        data["updated_at"] = datetime.now().isoformat()

        storage[session_id] = data

        self._write(storage)


    def load(self, session_id):

        storage = self._read()

        return storage.get(
            session_id,
            {}
        )


class MemoryManager:


    def __init__(self):

        self.store = MemoryStore()


    def remember(self, session_id, data):

        self.store.save(
            session_id,
            data
        )


    def recall(self, session_id):

        return self.store.load(
            session_id
        )


    def exists(self, session_id):

        return bool(
            self.recall(session_id)
        )

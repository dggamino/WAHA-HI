"""
Persistent Execution Store Foundation v0.1.0

Persistencia de eventos de ejecución del Companion Engine.
"""

import json
from pathlib import Path


class ExecutionStore:


    def __init__(
        self,
        path="data/execution_history.json"
    ):

        self.path = Path(path)

        self.path.parent.mkdir(
            exist_ok=True
        )

        if not self.path.exists():

            self.path.write_text(
                "[]",
                encoding="utf-8"
            )


    def _read(self):

        return json.loads(
            self.path.read_text(
                encoding="utf-8"
            )
        )


    def _write(
        self,
        data
    ):

        self.path.write_text(
            json.dumps(
                data,
                indent=2,
                ensure_ascii=False
            ),
            encoding="utf-8"
        )


    def append(
        self,
        event
    ):

        history = self._read()

        history.append(
            event
        )

        self._write(
            history
        )


    def all(self):

        return self._read()


    def clear(self):

        self._write([])

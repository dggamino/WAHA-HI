#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "=== IMPLEMENTAR 009 — Event Ledger Foundation v0.1.0 ==="

mkdir -p ledger
mkdir -p data


touch ledger/__init__.py


cat > ledger/models.py <<'EOF'
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Event:

    id: str
    event_type: str
    source: str
    payload: str
    created_at: str = ""


    def __post_init__(self):

        if not self.created_at:

            self.created_at = datetime.now().isoformat()
EOF


cat > ledger/sqlite.py <<'EOF'
import sqlite3
from pathlib import Path


DB_PATH = Path("data/events.db")


class EventLedger:


    def __init__(self):

        self.connection = sqlite3.connect(
            DB_PATH
        )

        self.create_table()



    def create_table(self):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS events (

                id TEXT PRIMARY KEY,

                event_type TEXT,

                source TEXT,

                payload TEXT,

                created_at TEXT

            )
            """
        )

        self.connection.commit()



    def append(self, event):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO events
            VALUES (?, ?, ?, ?, ?)
            """,

            (
                event.id,
                event.event_type,
                event.source,
                event.payload,
                event.created_at
            )

        )

        self.connection.commit()

        return event



    def list_events(self):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM events
            ORDER BY created_at
            """
        )

        return cursor.fetchall()
EOF


cat > ledger/service.py <<'EOF'
import uuid

from .models import Event
from .sqlite import EventLedger


class LedgerService:


    def __init__(self):

        self.db = EventLedger()



    def record(
        self,
        event_type,
        source,
        payload
    ):

        event = Event(

            id=str(uuid.uuid4()),

            event_type=event_type,

            source=source,

            payload=str(payload)

        )

        return self.db.append(
            event
        )



    def history(self):

        return self.db.list_events()
EOF


cat > ledger/events.py <<'EOF'
MESSAGE_RECEIVED = "MESSAGE_RECEIVED"

INTENT_DETECTED = "INTENT_DETECTED"

FLOW_EXECUTED = "FLOW_EXECUTED"

PROSPECT_CREATED = "PROSPECT_CREATED"

CRM_UPDATED = "CRM_UPDATED"

RESPONSE_GENERATED = "RESPONSE_GENERATED"
EOF


cat > ledger/README.md <<'EOF'
# Event Ledger Foundation

Registro histórico de eventos.

Responsabilidades:

- Auditoría técnica.
- Trazabilidad.
- Historial operativo.

No contiene:
- conocimiento.
- lógica conversacional.
- reglas comerciales.
EOF


echo ""
echo "=== VALIDACION LEDGER ==="

python3 - <<'EOF'

from ledger.service import LedgerService
from ledger.events import MESSAGE_RECEIVED


ledger = LedgerService()


event = ledger.record(

    MESSAGE_RECEIVED,

    "waha",

    {
        "text":
        "Quiero conocer HEREDITARIA"
    }

)


print(event)

print("")
print(ledger.history())

EOF


echo ""
echo "=== IMPLEMENTAR 009 COMPLETADO ==="

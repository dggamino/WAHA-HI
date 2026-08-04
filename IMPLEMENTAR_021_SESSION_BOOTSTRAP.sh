#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "=== IMPLEMENTAR 021 — Persistent Session Management Foundation v0.1.0 ==="

mkdir -p sessions


touch sessions/__init__.py


cat > sessions/__init__.py <<'EOF'
"""
Persistent Session Layer
"""
EOF


cat > sessions/models.py <<'EOF'
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class SessionRecord:

    session_id: str
    channel: str
    user_id: str
    state: dict

    created_at: str = ""
    updated_at: str = ""


    def __post_init__(self):

        now = datetime.now().isoformat()

        if not self.created_at:
            self.created_at = now

        if not self.updated_at:
            self.updated_at = now


    def serialize(self):

        return asdict(self)
EOF


cat > sessions/store.py <<'EOF'
import json
import os


SESSION_FILE = "data/sessions.json"


class SessionStore:


    def __init__(self):

        os.makedirs(
            "data",
            exist_ok=True
        )

        if not os.path.exists(
            SESSION_FILE
        ):

            with open(
                SESSION_FILE,
                "w"
            ) as file:

                json.dump(
                    {},
                    file
                )



    def save(self, session):

        sessions = self.all()

        sessions[
            session.session_id
        ] = session.serialize()


        with open(
            SESSION_FILE,
            "w"
        ) as file:

            json.dump(
                sessions,
                file,
                indent=2
            )



    def get(self, session_id):

        sessions = self.all()

        return sessions.get(
            session_id
        )



    def all(self):

        with open(
            SESSION_FILE
        ) as file:

            return json.load(
                file
            )
EOF


cat > sessions/service.py <<'EOF'
import uuid

from sessions.models import SessionRecord
from sessions.store import SessionStore



class SessionService:


    def __init__(self):

        self.store = SessionStore()



    def create(
        self,
        user_id,
        channel="whatsapp"
    ):

        session = SessionRecord(

            session_id=str(
                uuid.uuid4()
            ),

            channel=channel,

            user_id=user_id,

            state={}

        )


        self.store.save(
            session
        )


        return session



    def update_state(
        self,
        session_id,
        key,
        value
    ):

        data = self.store.get(
            session_id
        )


        if not data:

            return None


        data["state"][key] = value


        with open(
            "data/sessions.json",
            "w"
        ) as file:

            import json

            sessions = self.store.all()

            sessions[session_id] = data

            json.dump(
                sessions,
                file,
                indent=2
            )


        return data
EOF


cat > sessions/README.md <<'EOF'
# Persistent Session Management

Administra:

- Sesiones WhatsApp.
- Estado conversacional.
- Recuperación posterior.

No administra:

- conocimiento.
- CRM.
- campañas.
EOF


echo ""
echo "=== VALIDACION SESSION MANAGEMENT ==="

python3 - <<'EOF'

from sessions.service import SessionService


service = SessionService()


session = service.create(
    "5210000000000"
)


print(
    session.serialize()
)


print(
    service.update_state(
        session.session_id,
        "intent",
        "book_interest"
    )
)

EOF


echo ""
echo "=== IMPLEMENTAR 021 COMPLETADO ==="

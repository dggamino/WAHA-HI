#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "=== IMPLEMENTAR 005 — WAHA Adapter Contract v0.1.0 ==="

mkdir -p automation/waha


touch automation/__init__.py
touch automation/waha/__init__.py


cat > automation/waha/__init__.py <<'EOF'
"""
WAHA integration adapter layer.
"""
EOF


cat > automation/waha/models.py <<'EOF'
from dataclasses import dataclass


@dataclass
class IncomingMessage:

    session_id: str
    sender: str
    text: str
    channel: str = "whatsapp"



@dataclass
class OutgoingMessage:

    recipient: str
    text: str
    channel: str = "whatsapp"
EOF


cat > automation/waha/client.py <<'EOF'
"""
WAHA Client placeholder.

Future implementation:
HTTP requests to WAHA API.
"""


class WAHAClient:


    def send_message(self, recipient, text):

        return {

            "status": "queued",

            "recipient": recipient,

            "text": text

        }
EOF


cat > automation/waha/adapter.py <<'EOF'
"""
Transport adapter.

Transforms WAHA payloads into Companion requests.
"""


from automation.waha.models import (
    IncomingMessage,
    OutgoingMessage
)

from companion.engine import process



class WAHAAdapter:


    def receive(self, payload):

        message = IncomingMessage(

            session_id=payload.get(
                "session_id",
                "unknown"
            ),

            sender=payload.get(
                "sender",
                "unknown"
            ),

            text=payload.get(
                "text",
                ""
            )

        )


        result = process(

            message.text,

            message.session_id

        )


        return OutgoingMessage(

            recipient=message.sender,

            text=result["content"]

        )

EOF


cat > automation/waha/README.md <<'EOF'
# WAHA Adapter

Capa de integración WhatsApp.

Responsabilidades:

- Recibir eventos WAHA.
- Transformar payload.
- Enviar mensajes a Companion.
- Devolver respuesta estructurada.

No contiene conocimiento.
No contiene lógica conversacional.
EOF



echo ""
echo "=== VALIDACION WAHA CONTRACT ==="


python3 - <<'EOF'

from automation.waha.adapter import WAHAAdapter


payload = {

    "session_id": "demo-waha-001",

    "sender": "5210000000000",

    "text": "Quiero conocer los libros HEREDITARIA"

}


adapter = WAHAAdapter()


response = adapter.receive(payload)


print(response)


EOF


echo ""
echo "=== IMPLEMENTAR 005 COMPLETADO ==="

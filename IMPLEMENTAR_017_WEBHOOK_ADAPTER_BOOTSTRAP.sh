#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "=== IMPLEMENTAR 017 — Webhook Adapter Foundation v0.1.0 ==="

mkdir -p automation/webhook


touch automation/webhook/__init__.py


cat > automation/webhook/__init__.py <<'EOF'
"""
Webhook Adapter Layer
"""
EOF


cat > automation/webhook/models.py <<'EOF'
from dataclasses import dataclass


@dataclass
class WebhookEvent:

    event: str
    sender: str
    text: str
    session: str = "default"
EOF


cat > automation/webhook/adapter.py <<'EOF'
"""
External webhook transformer.
"""


from automation.webhook.models import WebhookEvent
from api.server import APIServer



class WebhookAdapter:


    def __init__(self):

        self.api = APIServer()



    def receive(self, payload):


        event = WebhookEvent(

            event=payload.get(
                "event",
                "message"
            ),

            sender=payload.get(
                "sender",
                "unknown"
            ),

            text=payload.get(
                "text",
                ""
            ),

            session=payload.get(
                "session",
                "default"
            )

        )


        if event.event != "message":

            return {

                "status":
                "ignored",

                "event":
                event.event

            }



        return self.api.handle(

            "message",

            {

                "text":
                event.text,

                "phone":
                event.sender

            }

        )
EOF


cat > automation/webhook/README.md <<'EOF'
# Webhook Adapter Foundation

Entrada externa de eventos.

Responsabilidades:

- Recibir webhook.
- Normalizar payload.
- Entregar al API Gateway.

No contiene:

- lógica conversacional.
- conocimiento.
- CRM.
EOF


echo ""
echo "=== VALIDACION WEBHOOK ADAPTER ==="

python3 - <<'EOF'

from automation.webhook.adapter import WebhookAdapter


adapter = WebhookAdapter()


payload = {

    "event":
    "message",

    "sender":
    "5210000000000",

    "text":
    "Quiero conocer los libros HEREDITARIA",

    "session":
    "waha-demo"

}


response = adapter.receive(
    payload
)


print(response)

EOF


echo ""
echo "=== IMPLEMENTAR 017 COMPLETADO ==="

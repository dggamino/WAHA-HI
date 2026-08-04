#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "=== IMPLEMENTAR 002 — Companion Engine Foundation v0.1.0 ==="

mkdir -p companion/{intents,flows,responders,prompts}
mkdir -p logs

touch companion/__init__.py
touch companion/intents/__init__.py
touch companion/flows/__init__.py
touch companion/responders/__init__.py

cat > companion/__init__.py <<'EOF'
"""
WAHA-HI Companion Engine
Conversational orchestration layer.
"""
EOF

cat > companion/session.py <<'EOF'
from datetime import datetime
import uuid


class Session:
    def __init__(self, session_id=None, channel="unknown"):
        self.id = session_id or str(uuid.uuid4())
        self.channel = channel
        self.created_at = datetime.now()
        self.state = {}

    def to_dict(self):
        return {
            "id": self.id,
            "channel": self.channel,
            "created_at": self.created_at.isoformat(),
            "state": self.state
        }
EOF

cat > companion/context.py <<'EOF'
class Context:

    def __init__(self, session):
        self.session = session
        self.data = {
            "session_id": session.id,
            "intent": None,
            "flow": None,
            "metadata": {}
        }

    def update(self, key, value):
        self.data[key] = value
EOF

cat > companion/memory.py <<'EOF'
class Memory:

    def __init__(self):
        self.storage = {}

    def save(self, session_id, data):
        self.storage[session_id] = data

    def load(self, session_id):
        return self.storage.get(session_id, {})
EOF

cat > companion/intents/models.py <<'EOF'
from dataclasses import dataclass


@dataclass
class Intent:
    name: str
    description: str
EOF

cat > companion/intents/registry.py <<'EOF'
from .models import Intent


INTENTS = [
    Intent("book_interest", "Interés por libros"),
    Intent("consultation_request", "Solicitud de consulta"),
    Intent("caregiver_problem", "Problema relacionado con cuidado"),
    Intent("property_question", "Consulta patrimonial"),
    Intent("elderly_support", "Apoyo adulto mayor"),
    Intent("general_information", "Información general"),
    Intent("human_escalation", "Solicitar atención humana"),
    Intent("unknown", "No identificado"),
]


def list_intents():
    return INTENTS
EOF

cat > companion/intents/classifier.py <<'EOF'
def classify(message):

    text = message.lower()

    if "libro" in text or "libros" in text:
        return "book_interest"

    if "asesoría" in text or "consulta" in text:
        return "consultation_request"

    if "humano" in text or "persona" in text:
        return "human_escalation"

    return "unknown"
EOF

cat > companion/router.py <<'EOF'
from .flows import books, consultation, escalation


ROUTES = {
    "book_interest": books.handle,
    "consultation_request": consultation.handle,
    "human_escalation": escalation.handle,
}


def dispatch(intent, context):

    handler = ROUTES.get(intent)

    if handler:
        return handler(context)

    return {
        "type": "text",
        "content": "No pude identificar la solicitud."
    }
EOF

cat > companion/flows/books.py <<'EOF'
def handle(context):

    context.update("flow", "books")

    return {
        "type": "text",
        "content": "Información editorial HEREDITARIA disponible."
    }
EOF

cat > companion/flows/consultation.py <<'EOF'
def handle(context):

    context.update("flow", "consultation")

    return {
        "type": "text",
        "content": "Solicitud de consulta registrada."
    }
EOF

cat > companion/flows/escalation.py <<'EOF'
def handle(context):

    context.update("flow", "escalation")

    return {
        "type": "text",
        "content": "Solicitud enviada a atención humana."
    }
EOF

cat > companion/engine.py <<'EOF'
import logging
from pathlib import Path

from .session import Session
from .context import Context
from .router import dispatch
from .intents.classifier import classify
from .intents.registry import list_intents


logging.basicConfig(
    filename="logs/companion.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)


def load_prompts():

    prompt_path = Path("companion/prompts")

    prompts = list(prompt_path.glob("*.md"))

    logging.info(
        "PROMPTS_LOADED %s",
        len(prompts)
    )

    return prompts


def process(message, session_id=None):

    session = Session(
        session_id=session_id,
        channel="whatsapp"
    )

    context = Context(session)

    intent = classify(message)

    context.update(
        "intent",
        intent
    )

    response = dispatch(
        intent,
        context
    )

    return response


def main():

    logging.info("COMPANION_STARTED")

    session = Session(
        channel="demo"
    )

    logging.info(
        "SESSION_CREATED %s",
        session.id
    )

    load_prompts()

    intents = list_intents()

    logging.info(
        "INTENTS_REGISTERED %s",
        len(intents)
    )

    result = process(
        "Quiero conocer los libros HEREDITARIA",
        session.id
    )

    logging.info(
        "ROUTER_READY %s",
        result
    )

    print(result)


if __name__ == "__main__":
    main()
EOF

cat > companion/prompts/system.md <<'EOF'
Identidad del asistente conversacional.
EOF

cat > companion/prompts/assistant.md <<'EOF'
Reglas generales de interacción.
EOF

cat > companion/prompts/classifier.md <<'EOF'
Criterios de clasificación de intención.
EOF

cat > companion/prompts/style.md <<'EOF'
Estilo conversacional.
EOF

cat > companion/README.md <<'EOF'
# Companion Engine

Capa conversacional desacoplada de conocimiento.

No contiene contenido patrimonial.

Entrada:
WhatsApp / WAHA

Salida:
Acciones estructuradas.
EOF

echo ""
echo "=== VALIDACION ==="

python3 -m companion.engine

echo ""
echo "=== IMPLEMENTAR 002 COMPLETADO ==="

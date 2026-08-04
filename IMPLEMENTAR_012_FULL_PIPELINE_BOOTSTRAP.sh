#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "=== IMPLEMENTAR 012 — Full Pipeline Integration v0.1.0 ==="

mkdir -p pipeline


cat > pipeline/full_runtime.py <<'EOF'
"""
Full Event Driven Runtime

Integra:
- Companion
- Knowledge
- CRM
- Ledger
"""


from pipeline.events import PipelineEvent
from pipeline.bus import EventBus

from ledger.service import LedgerService
from ledger.events import (
    MESSAGE_RECEIVED,
    INTENT_DETECTED,
    FLOW_EXECUTED,
    CRM_UPDATED,
    RESPONSE_GENERATED
)

from companion.intents.classifier import classify
from companion.session import Session
from companion.context import Context
from companion.router import dispatch

from crm.service import CRMService
from crm.status import (
    BOOK_INTEREST,
    CONSULTATION_REQUESTED
)



class FullPipeline:


    def __init__(self):

        self.bus = EventBus()

        self.ledger = LedgerService()

        self.crm = CRMService()

        self.register()



    def register(self):

        self.bus.subscribe(
            MESSAGE_RECEIVED,
            self.message_received
        )



    def emit(
        self,
        event_type,
        payload
    ):

        self.ledger.record(
            event_type,
            "pipeline",
            payload
        )



    def message_received(
        self,
        event
    ):

        self.emit(
            MESSAGE_RECEIVED,
            event.payload
        )


        text = event.payload["text"]


        intent = classify(text)


        self.emit(
            INTENT_DETECTED,
            {
                "intent": intent
            }
        )


        session = Session(
            channel="whatsapp"
        )


        context = Context(session)


        context.update(
            "intent",
            intent
        )


        context.update(
            "phone",
            event.payload.get(
                "phone",
                "unknown"
            )
        )


        response = dispatch(
            intent,
            context
        )


        self.emit(
            FLOW_EXECUTED,
            response
        )


        prospect = self.crm.create_prospect(
            context.data["phone"]
        )


        if intent == "book_interest":

            self.crm.update_status(
                prospect.id,
                BOOK_INTEREST
            )


        elif intent == "consultation_request":

            self.crm.update_status(
                prospect.id,
                CONSULTATION_REQUESTED
            )


        self.emit(
            CRM_UPDATED,
            {
                "prospect_id": prospect.id,
                "intent": intent
            }
        )


        self.emit(
            RESPONSE_GENERATED,
            response
        )


        return response



    def process(
        self,
        text,
        phone
    ):

        event = PipelineEvent(

            MESSAGE_RECEIVED,

            {
                "text": text,
                "phone": phone
            }

        )


        return self.message_received(
            event
        )
EOF


echo ""
echo "=== VALIDACION FULL PIPELINE ==="

python3 - <<'EOF'

from pipeline.full_runtime import FullPipeline


pipeline = FullPipeline()


result = pipeline.process(
    "Quiero conocer los libros HEREDITARIA",
    "5210000000000"
)


print(result)

EOF


echo ""
echo "=== IMPLEMENTAR 012 COMPLETADO ==="

from ledger.service import LedgerService
from ledger.events import (
    MESSAGE_RECEIVED,
    INTENT_DETECTED,
    RESPONSE_GENERATED
)

from companion.intents.classifier import classify


ledger = LedgerService()



def on_message_received(event):

    ledger.record(

        MESSAGE_RECEIVED,

        "pipeline",

        event.payload

    )


    intent = classify(

        event.payload.get(
            "text",
            ""
        )

    )


    return {

        "intent": intent

    }



def on_intent_detected(event):

    ledger.record(

        INTENT_DETECTED,

        "pipeline",

        event.payload

    )


    return event.payload



def on_response_generated(event):

    ledger.record(

        RESPONSE_GENERATED,

        "pipeline",

        event.payload

    )


    return event.payload

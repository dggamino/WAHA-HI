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


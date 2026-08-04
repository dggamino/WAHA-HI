"""
WAHA Session Bridge Foundation v0.1.0
"""

from .client import WAHAClient
from ...pipeline import CompanionPipeline
from ...session import Session


class WAHAAdapter:

    def __init__(self):

        self.client = WAHAClient()
        self.pipeline = CompanionPipeline()


    def receive(self, event):

        chat_id = event.get(
            "chat_id",
            ""
        )

        message = event.get(
            "message",
            ""
        )

        session = Session(
            session_id=chat_id,
            channel="whatsapp"
        )

        result = self.pipeline.handle(
            message,
            session=session
        )

        return self.client.send_message(
            chat_id,
            result["response"]
        )

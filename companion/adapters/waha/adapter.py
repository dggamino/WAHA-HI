"""
WAHA Adapter Foundation v0.1.0
"""

from .client import WAHAClient
from ...pipeline import CompanionPipeline


class WAHAAdapter:

    def __init__(self):
        self.client = WAHAClient()
        self.pipeline = CompanionPipeline()

    def receive(self, event):

        message = event.get("message", "")
        chat_id = event.get("chat_id", "")

        result = self.pipeline.handle(
            message
        )

        return self.client.send_message(
            chat_id,
            result["response"]
        )

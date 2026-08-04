"""
WAHA Client Foundation v0.1.0
"""


class WAHAClient:

    def send_message(self, chat_id, text):

        return {
            "status": "sent",
            "chat_id": chat_id,
            "text": text
        }

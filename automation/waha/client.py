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

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

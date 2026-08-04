from pipeline.bus import EventBus
from pipeline.events import PipelineEvent
from pipeline.handlers import (
    on_message_received,
    on_intent_detected,
    on_response_generated
)


class PipelineRuntime:


    def __init__(self):

        self.bus = EventBus()

        self.register()



    def register(self):

        self.bus.subscribe(

            "MESSAGE_RECEIVED",

            on_message_received

        )


        self.bus.subscribe(

            "INTENT_DETECTED",

            on_intent_detected

        )


        self.bus.subscribe(

            "RESPONSE_GENERATED",

            on_response_generated

        )



    def process(self, text):

        event = PipelineEvent(

            "MESSAGE_RECEIVED",

            {
                "text": text
            }

        )


        return self.bus.publish(
            event
        )

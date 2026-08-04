"""
Simple internal event bus.
"""


class EventBus:


    def __init__(self):

        self.handlers = {}



    def subscribe(self, event_type, handler):

        if event_type not in self.handlers:

            self.handlers[event_type] = []

        self.handlers[event_type].append(handler)



    def publish(self, event):

        handlers = self.handlers.get(
            event.event_type,
            []
        )

        results = []

        for handler in handlers:

            results.append(
                handler(event)
            )

        return results

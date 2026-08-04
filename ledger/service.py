import uuid

from .models import Event
from .sqlite import EventLedger


class LedgerService:


    def __init__(self):

        self.db = EventLedger()



    def record(
        self,
        event_type,
        source,
        payload
    ):

        event = Event(

            id=str(uuid.uuid4()),

            event_type=event_type,

            source=source,

            payload=str(payload)

        )

        return self.db.append(
            event
        )



    def history(self):

        return self.db.list_events()

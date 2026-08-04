from dataclasses import dataclass
from datetime import datetime


@dataclass
class Event:

    id: str
    event_type: str
    source: str
    payload: str
    created_at: str = ""


    def __post_init__(self):

        if not self.created_at:

            self.created_at = datetime.now().isoformat()

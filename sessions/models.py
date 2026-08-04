from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class SessionRecord:

    session_id: str
    channel: str
    user_id: str
    state: dict

    created_at: str = ""
    updated_at: str = ""


    def __post_init__(self):

        now = datetime.now().isoformat()

        if not self.created_at:
            self.created_at = now

        if not self.updated_at:
            self.updated_at = now


    def serialize(self):

        return asdict(self)

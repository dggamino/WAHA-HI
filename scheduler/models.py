from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class FollowUpTask:

    task_id: str
    prospect_id: str
    action: str
    status: str
    scheduled_at: str


    def serialize(self):

        return asdict(self)

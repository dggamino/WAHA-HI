from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class NotificationTask:

    notification_id: str
    task_id: str
    channel: str
    recipient: str
    content: str
    status: str
    attempts: int
    created_at: str


    def serialize(self):

        return asdict(self)

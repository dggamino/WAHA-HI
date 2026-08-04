from datetime import datetime
import uuid


class Session:
    def __init__(self, session_id=None, channel="unknown"):
        self.id = session_id or str(uuid.uuid4())
        self.channel = channel
        self.created_at = datetime.now()
        self.state = {}

    def to_dict(self):
        return {
            "id": self.id,
            "channel": self.channel,
            "created_at": self.created_at.isoformat(),
            "state": self.state
        }

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

class SessionMemory:

    def __init__(self, session, memory):

        self.session = session
        self.memory = memory


    def save_state(self):

        self.memory.remember(
            self.session.id,
            self.session.state
        )


    def load_state(self):

        self.session.state = self.memory.recall(
            self.session.id
        )

        return self.session.state

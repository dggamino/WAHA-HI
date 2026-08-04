from dataclasses import dataclass
from datetime import datetime
import uuid


@dataclass
class PipelineEvent:

    event_type: str
    payload: dict

    id: str = ""
    created_at: str = ""


    def __post_init__(self):

        if not self.id:
            self.id = str(uuid.uuid4())

        if not self.created_at:
            self.created_at = datetime.now().isoformat()

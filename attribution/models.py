from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class AttributionRecord:

    prospect_id: str
    campaign: str
    channel: str
    source: str
    created_at: str = ""


    def __post_init__(self):

        if not self.created_at:

            self.created_at = datetime.now().isoformat()


    def serialize(self):

        return asdict(self)

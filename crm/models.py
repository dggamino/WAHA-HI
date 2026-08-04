from dataclasses import dataclass
from datetime import datetime


@dataclass
class Prospect:

    id: str
    phone: str
    name: str = ""
    status: str = "NEW"
    created_at: str = ""


    def __post_init__(self):

        if not self.created_at:
            self.created_at = datetime.now().isoformat()

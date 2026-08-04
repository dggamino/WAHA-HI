from dataclasses import dataclass
from datetime import datetime


@dataclass
class AutomationResult:

    workflow: str
    status: str
    action: str
    created_at: str = ""


    def __post_init__(self):

        if not self.created_at:

            self.created_at = datetime.now().isoformat()


    def serialize(self):

        return {

            "workflow": self.workflow,

            "status": self.status,

            "action": self.action,

            "created_at": self.created_at

        }

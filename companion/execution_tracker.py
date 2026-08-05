"""
Execution Tracking Foundation v0.1.0

Registra el ciclo de vida de ejecución del Companion Engine.
"""

from datetime import datetime


class ExecutionTracker:


    def __init__(self):

        self.events = []



    def timestamp(self):

        return datetime.utcnow().isoformat()



    def create(
        self,
        plan,
        session_id=None
    ):

        event = {
            "status": "CREATED",
            "session_id": session_id,
            "goal": plan.get(
                "goal",
                "unknown"
            ),
            "actions": plan.get(
                "actions",
                []
            ),
            "created_at": self.timestamp()
        }

        self.events.append(event)

        return event



    def start(
        self,
        event
    ):

        event["status"] = "STARTED"

        event["started_at"] = self.timestamp()

        return event



    def complete(
        self,
        event,
        result=None
    ):

        event["status"] = "COMPLETED"

        event["completed_at"] = self.timestamp()

        event["result"] = result

        return event



    def fail(
        self,
        event,
        error
    ):

        event["status"] = "FAILED"

        event["error"] = str(error)

        event["failed_at"] = self.timestamp()

        return event



    def history(self):

        return self.events

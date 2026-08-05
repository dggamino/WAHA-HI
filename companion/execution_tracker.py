"""
Execution Tracking Foundation v0.2.0

Sistema persistente de seguimiento de ejecución.
IMPLEMENTAR 029
"""

from datetime import datetime

from .execution_store import ExecutionStore



class ExecutionTracker:


    def __init__(self):

        self.store = ExecutionStore()



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


        self.store.append(
            event
        )


        return event



    def persist(
        self,
        event
    ):

        self.store.append(
            event
        )

        return event



    def start(
        self,
        event
    ):

        event["status"] = "STARTED"

        event["started_at"] = self.timestamp()

        self.persist(
            event
        )

        return event



    def complete(
        self,
        event,
        result=None
    ):

        event["status"] = "COMPLETED"

        event["completed_at"] = self.timestamp()

        event["result_summary"] = {

            "status": result.get(
                "status"
            )
            if isinstance(result, dict)
            else None,

            "flow": result.get(
                "flow"
            )
            if isinstance(result, dict)
            else None

        }


        self.persist(
            event
        )

        return event



    def fail(
        self,
        event,
        error
    ):

        event["status"] = "FAILED"

        event["error"] = str(error)

        event["failed_at"] = self.timestamp()


        self.persist(
            event
        )

        return event



    def history(self):

        return self.store.all()

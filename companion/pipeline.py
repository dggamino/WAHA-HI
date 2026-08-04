"""
Companion Pipeline Integration Foundation v0.2.0
"""

from .intents.classifier import classify
from .flows import FlowOrchestrator
from .responders import get_responder
from .memory import MemoryManager
from .session import Session


class CompanionPipeline:

    def __init__(self):

        self.orchestrator = FlowOrchestrator()
        self.responder = get_responder()
        self.memory = MemoryManager()


    def handle(
        self,
        message,
        context=None,
        session=None,
        session_id=None
    ):

        if session is None:
            session = Session(
                session_id=session_id,
                channel="internal"
            )

        previous = self.memory.recall(
            session.id
        )

        if context is None:
            context = {}

        context["memory"] = previous

        intent = classify(
            message
        )

        result = self.orchestrator.route(
            intent,
            context
        )

        session.state = {
            "last_message": message,
            "last_intent": intent
        }

        self.memory.remember(
            session.id,
            session.state
        )

        response = self.responder.build(
            result
        )

        return {
            "intent": intent,
            "result": result,
            "response": response,
            "memory": previous,
            "session_id": session.id
        }

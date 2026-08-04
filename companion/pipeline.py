"""
Companion Pipeline Integration Foundation v0.2.0
"""

from .intents.classifier import classify
from .flows import FlowOrchestrator
from .responders import get_responder
from .memory import MemoryManager


class CompanionPipeline:

    def __init__(self):

        self.orchestrator = FlowOrchestrator()
        self.responder = get_responder()
        self.memory = MemoryManager()


    def handle(self, message, context=None, session_id="default"):

        previous = self.memory.recall(
            session_id
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

        self.memory.remember(
            session_id,
            {
                "last_message": message,
                "last_intent": intent
            }
        )

        response = self.responder.build(
            result
        )

        return {
            "intent": intent,
            "result": result,
            "response": response,
            "memory": previous
        }

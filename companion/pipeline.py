"""
Companion Pipeline Integration Foundation v0.1.0
"""

from .intents.classifier import classify
from .flows import FlowOrchestrator
from .responders import get_responder


class CompanionPipeline:

    def __init__(self):
        self.orchestrator = FlowOrchestrator()
        self.responder = get_responder()

    def handle(self, message, context=None):

        intent = classify(message)

        result = self.orchestrator.route(
            intent,
            context
        )

        response = self.responder.build(
            result
        )

        return {
            "intent": intent,
            "result": result,
            "response": response
        }

"""
Companion Pipeline Integration Foundation v0.2.0
"""

from .intents.classifier import classify
from .flows import FlowOrchestrator
from .responders import get_responder
from .session import Session
from .context import ContextLifecycleManager


class CompanionPipeline:


    def __init__(self):

        self.orchestrator = FlowOrchestrator()
        self.responder = get_responder()
        self.context_manager = ContextLifecycleManager()


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


        if context is None:

            context = self.context_manager.create_context(
                session
            )


        intent = classify(
            message
        )


        self.context_manager.update_context(
            context,
            intent=intent,
            state="INTENT_DETECTED"
        )


        result = self.orchestrator.route(
            intent,
            context
        )


        self.context_manager.update_context(
            context,
            state="FLOW_ACTIVE"
        )


        response = self.responder.build(
            result
        )


        self.context_manager.persist_context(
            context
        )


        return {
            "intent": intent,
            "result": result,
            "response": response,
            "context": context.to_dict(),
            "session_id": session.id
        }

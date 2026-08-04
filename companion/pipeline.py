"""
Companion Pipeline Integration Foundation v0.3.0
IMPLEMENTAR 020: Pipeline Multi-Turn Resolver Integration Foundation v0.1.0
"""

from .intents.classifier import classify
from .flows import FlowOrchestrator
from .responders import get_responder
from .session import Session
from .context import (
    ContextLifecycleManager,
    ConversationResolver,
)


class CompanionPipeline:

    def __init__(self):

        self.orchestrator = FlowOrchestrator()
        self.responder = get_responder()
        self.context_manager = ContextLifecycleManager()
        self.resolver = ConversationResolver()


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

            stored = self.context_manager.load_context(
                session.id
            )

            if stored:

                context = self.context_manager.create_context(
                    session
                )

                context.intent = stored.get(
                    "intent",
                    ""
                )

                context.memory = stored.get(
                    "memory",
                    {}
                )

                context.knowledge = stored.get(
                    "knowledge",
                    []
                )

            else:

                context = self.context_manager.create_context(
                    session
                )


        context_data = context.to_dict()


        resolved_message = self.resolver.resolve(
            message,
            context_data
        )


        intent = classify(
            resolved_message
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
            "message": resolved_message,
            "result": result,
            "response": response,
            "context": context.to_dict(),
            "session_id": session.id
        }

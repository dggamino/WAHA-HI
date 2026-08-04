"""
Companion Pipeline Integration Foundation v0.4.0

IMPLEMENTAR 022:
Pipeline Memory Intelligence Integration Foundation v0.1.0
"""

from .intents.classifier import classify
from .flows import FlowOrchestrator
from .responders import get_responder
from .session import Session

from .context import (
    ContextLifecycleManager,
    ConversationResolver,
)

from .memory_intelligence import MemoryIntelligence


class CompanionPipeline:


    def __init__(self):

        self.orchestrator = FlowOrchestrator()
        self.responder = get_responder()

        self.context_manager = ContextLifecycleManager()
        self.resolver = ConversationResolver()

        self.memory_intelligence = MemoryIntelligence()


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


        intelligent_memory = self.memory_intelligence.enrich(
            message,
            intent,
            result
        )


        context.memory = intelligent_memory


        self.context_manager.persist_context(
            context
        )


        return {

            "intent": intent,

            "message": resolved_message,

            "result": result,

            "response": response,

            "memory": intelligent_memory,

            "context": context.to_dict(),

            "session_id": session.id

        }

"""
Companion Pipeline Integration Foundation v0.6.0

IMPLEMENTAR 024:
Pipeline Semantic Memory Retrieval Integration Foundation v0.2.0
"""

from .intents.classifier import classify
from .flows import FlowOrchestrator
from .responders import get_responder
from .session import Session

from .context import (
    ContextLifecycleManager,
    ConversationResolver,
)

from .memory import MemoryManager
from .memory_intelligence import MemoryIntelligence
from .semantic_memory import SemanticMemoryRetriever


class CompanionPipeline:


    def __init__(self):

        self.orchestrator = FlowOrchestrator()
        self.responder = get_responder()

        self.context_manager = ContextLifecycleManager()
        self.resolver = ConversationResolver()

        self.memory_manager = MemoryManager()

        self.semantic_memory = SemanticMemoryRetriever(
            self.memory_manager
        )

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


        semantic_memory = self.semantic_memory.retrieve(
            session.id,
            message
        )


        if context is None:

            context = self.context_manager.create_context(
                session
            )


        context_data = context.to_dict()


        # Inyección explícita de memoria semántica
        if semantic_memory:

            context_data["memory"] = semantic_memory

            if not context_data.get("intent"):

                context_data["intent"] = semantic_memory.get(
                    "last_intent",
                    ""
                )


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


        self.memory_manager.remember(
            session.id,
            intelligent_memory
        )


        return {

            "intent": intent,

            "message": resolved_message,

            "result": result,

            "response": response,

            "memory": intelligent_memory,

            "semantic_memory": semantic_memory,

            "context": context.to_dict(),

            "session_id": session.id

        }

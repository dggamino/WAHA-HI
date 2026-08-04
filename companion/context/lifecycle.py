"""
Context Lifecycle Manager Foundation v0.1.0
"""

from companion.context.models import ConversationContext
from companion.context.persistence import ContextMemoryBridge


class ContextLifecycleManager:


    def __init__(self):

        self.bridge = ContextMemoryBridge()


    def create_context(
        self,
        session,
        user_id="",
        intent=""
    ):

        context = ConversationContext(
            session_id=session.id,
            user_id=user_id,
            intent=intent
        )

        self.bridge.save_context(
            context
        )

        return context


    def load_context(
        self,
        session_id
    ):

        return self.bridge.load_context(
            session_id
        )


    def update_context(
        self,
        context,
        state=None,
        intent=None
    ):

        if state:
            context.update_state(
                state
            )

        if intent:
            context.intent = intent

        self.bridge.save_context(
            context
        )

        return context


    def persist_context(
        self,
        context
    ):

        return self.bridge.save_context(
            context
        )

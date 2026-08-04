"""
Conversation Context Service.
"""

from companion.context.merge import ContextMerger
from companion.states.machine import ConversationStateMachine


class ContextService:


    def __init__(self):

        self.merger = ContextMerger()


    def create_context(
        self,
        session,
        intent,
        query
    ):

        context = self.merger.build(
            session,
            intent,
            query
        )

        machine = ConversationStateMachine()

        context.update_state(
            machine.current_state()
        )

        return context

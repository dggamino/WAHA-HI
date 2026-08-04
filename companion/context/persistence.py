"""
Context Memory Synchronization Foundation v0.1.0
"""

from companion.memory import MemoryManager


class ContextMemoryBridge:


    def __init__(self):

        self.memory = MemoryManager()


    def save_context(self, context):

        self.memory.remember(
            context.session_id,
            context.to_dict()
        )

        return True


    def load_context(self, session_id):

        data = self.memory.recall(
            session_id
        )

        return data


    def sync_state(self, context):

        return self.save_context(
            context
        )

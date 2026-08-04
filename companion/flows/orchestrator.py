"""
Flow Orchestrator Foundation v0.1.0
"""

from .registry import get_flow


class FlowOrchestrator:

    def route(self, intent, context):
        flow = get_flow(intent)

        if not flow:
            return {
                "status": "no_flow",
                "intent": intent
            }

        return flow.execute(context)

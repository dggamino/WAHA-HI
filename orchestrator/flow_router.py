"""
Dynamic flow selector.
"""


from orchestrator.flows.registry import get_flow



class FlowOrchestrator:


    def execute(
        self,
        intent,
        context
    ):


        flow = get_flow(
            intent
        )


        if not flow:

            return {

                "type":
                "text",

                "content":
                "No existe flujo disponible."

            }


        return flow.execute(
            context
        )

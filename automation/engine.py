"""
Automation orchestration engine.
"""


from automation.workflows.registry import get_workflow
from automation.actions.executor import ActionExecutor



class AutomationEngine:


    def __init__(self):

        self.executor = ActionExecutor()



    def process(self, event):

        workflow = get_workflow(
            event[1]
            if isinstance(event, tuple)
            else event.event_type
        )


        if not workflow:

            return None



        return self.executor.execute(
            workflow
        )

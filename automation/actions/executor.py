from automation.models import AutomationResult



class ActionExecutor:


    def execute(self, workflow):

        return AutomationResult(

            workflow=
            workflow["workflow"],

            status=
            "executed",

            action=
            workflow["action"]

        )

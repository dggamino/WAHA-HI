"""
Internal API Router.
"""


from dashboard.service import DashboardService
from pipeline.full_runtime import FullPipeline



class APIRouter:


    def __init__(self):

        self.pipeline = FullPipeline()

        self.dashboard = DashboardService()



    def execute(self, request):


        if request.action == "message":


            result = self.pipeline.process(

                request.payload.get(
                    "text",
                    ""
                ),

                request.payload.get(
                    "phone",
                    "unknown"
                )

            )


            return {

                "status":
                "success",

                "response":
                result

            }



        if request.action == "dashboard":


            return {

                "status":
                "success",

                "dashboard":
                self.dashboard.snapshot()

            }



        return {

            "status":
            "error",

            "message":
            "unknown_action"

        }

"""
Dashboard presentation layer.
"""


class DashboardView:


    def render(self, metrics):

        return {

            "dashboard":

            {

                "total_events":
                metrics.get(
                    "total_events",
                    0
                ),

                "messages":
                metrics.get(
                    "messages_received",
                    0
                ),

                "intents":
                metrics.get(
                    "intents_detected",
                    0
                ),

                "flows":
                metrics.get(
                    "flows_executed",
                    0
                ),

                "leads":
                metrics.get(
                    "leads_created",
                    0
                )

            }

        }

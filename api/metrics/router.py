from api.metrics.service import MetricsService



class MetricsRouter:


    def __init__(self):

        self.service = MetricsService()



    def get_metrics(self):

        return {

            "status": "success",

            "metrics":
                self.service.current()

        }

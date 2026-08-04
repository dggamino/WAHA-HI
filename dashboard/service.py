from api.metrics.router import MetricsRouter
from dashboard.view import DashboardView



class DashboardService:


    def __init__(self):

        self.metrics = MetricsRouter()

        self.view = DashboardView()



    def status(self):

        response = self.metrics.get_metrics()


        return self.view.render(

            response["metrics"]

        )

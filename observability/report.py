"""
Unified diagnostic report.
"""


from observability.health import HealthMonitor
from observability.events import EventMonitor
from analytics.service import AnalyticsService



class DiagnosticReport:


    def __init__(self):

        self.health = HealthMonitor()

        self.events = EventMonitor()

        self.analytics = AnalyticsService()



    def generate(self):

        return {

            "health":
            self.health.check(),

            "metrics":
            self.analytics.report(),

            "recent_events":
            self.events.recent()

        }

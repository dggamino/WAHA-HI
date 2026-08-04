from analytics.collector import AnalyticsCollector


class AnalyticsService:


    def __init__(self):

        self.collector = AnalyticsCollector()



    def generate(self, events):

        return self.collector.collect(
            events
        )

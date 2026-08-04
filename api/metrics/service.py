from ledger.service import LedgerService
from analytics.service import AnalyticsService


class MetricsService:


    def __init__(self):

        self.ledger = LedgerService()

        self.analytics = AnalyticsService()



    def current(self):

        events = list(
            self.ledger.history()
        )

        report = self.analytics.generate(
            events
        )

        return report.serialize()

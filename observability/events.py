"""
Event inspection.
"""


from ledger.service import LedgerService



class EventMonitor:


    def __init__(self):

        self.ledger = LedgerService()



    def recent(self, limit=10):

        events = self.ledger.history()

        return events[-limit:]

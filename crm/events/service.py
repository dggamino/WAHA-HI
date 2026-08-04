from crm.events.publisher import CRMEventPublisher



class CRMEventService:


    def __init__(self, ledger):

        self.publisher = CRMEventPublisher(
            ledger
        )



    def sync_prospect(self, prospect):

        return self.publisher.prospect_created(
            prospect
        )

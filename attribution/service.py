from attribution.repository import AttributionRepository



class AttributionService:


    def __init__(self):

        self.repository = AttributionRepository()



    def register(self, record):

        return self.repository.save(
            record
        )

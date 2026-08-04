"""
Campaign attribution engine.
"""


from attribution.models import AttributionRecord



class AttributionEngine:


    def attribute(

        self,

        prospect_id,

        campaign="organic",

        channel="whatsapp",

        source="conversation"

    ):


        return AttributionRecord(

            prospect_id=prospect_id,

            campaign=campaign,

            channel=channel,

            source=source

        )

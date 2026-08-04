from .registry import get_campaign


class CampaignService:


    def resolve(self, campaign_id):

        campaign = get_campaign(
            campaign_id
        )


        if not campaign:

            return {

                "status":
                "NOT_FOUND"

            }


        return {

            "status":
            "FOUND",

            "campaign":
            campaign

        }

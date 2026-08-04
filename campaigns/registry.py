"""
HEREDITARIA Campaign Registry
"""


CAMPAIGNS = {


    "HER-BOOK-001": {

        "name":
        "Libro Fundacional HEREDITARIA",

        "asset":
        "fundacional",

        "source":
        "whatsapp"

    },


    "HER-BOOK-002": {

        "name":
        "Libro del Cuidador",

        "asset":
        "cuidador",

        "source":
        "whatsapp"

    },


    "HER-BOOK-003": {

        "name":
        "Libro del Patrimonio Invisible",

        "asset":
        "patrimonio",

        "source":
        "whatsapp"

    }


}


def get_campaign(campaign_id):

    return CAMPAIGNS.get(
        campaign_id
    )


def list_campaigns():

    return CAMPAIGNS

"""
Qualification rules.
"""


def evaluate(intent):


    rules = {


        "book_interest":
        "warm",


        "consultation_request":
        "hot",


        "unknown":
        "cold"

    }


    return rules.get(
        intent,
        "cold"
    )

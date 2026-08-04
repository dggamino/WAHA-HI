"""
Flow registry.
"""


from companion.flows.books import BooksFlow
from companion.flows.consultation import ConsultationFlow



FLOWS = {

    "book_interest":
    BooksFlow(),

    "consultation_request":
    ConsultationFlow()

}



def get_flow(intent):

    return FLOWS.get(
        intent
    )

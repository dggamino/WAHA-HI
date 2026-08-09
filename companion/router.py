from .flows import books, consultation, escalation, greeting, help, status, caregiver, property, receipt, card, chapter

ROUTES = {
    "greeting": greeting.handle,
    "help": help.handle,
    "status": status.handle,
    "book_interest": books.handle,
    "consultation_request": consultation.handle,
    "human_escalation": escalation.handle,
    "caregiver_problem": caregiver.handle,
    "property_question": property.handle,
    "receipt_registration": receipt.handle,
    "card_trust": card.handle,
    "chapter_request": chapter.handle,
}


def dispatch(intent, context):
    handler = ROUTES.get(intent)
    if handler:
        return handler(context)
    return {
        "type": "text",
        "content": "No pude identificar la solicitud."
    }

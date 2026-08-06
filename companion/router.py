from .flows import books, consultation, escalation, greeting, help, status, caregiver, property


ROUTES = {
    "greeting": greeting.handle,
    "help": help.handle,
    "status": status.handle,
    "book_interest": books.handle,
    "consultation_request": consultation.handle,
    "human_escalation": escalation.handle,
    "caregiver_problem": caregiver.handle,
    "property_question": property.handle,
}


def dispatch(intent, context):

    handler = ROUTES.get(intent)

    if handler:
        return handler(context)

    return {
        "type": "text",
        "content": "No pude identificar la solicitud."
    }

from .flows import books, consultation, escalation


ROUTES = {
    "book_interest": books.handle,
    "consultation_request": consultation.handle,
    "human_escalation": escalation.handle,
}


def dispatch(intent, context):

    handler = ROUTES.get(intent)

    if handler:
        return handler(context)

    return {
        "type": "text",
        "content": "No pude identificar la solicitud."
    }

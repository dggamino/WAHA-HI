from .flows import books, consultation, escalation, greeting, help, status, caregiver, property, receipt, card, chapter
from .flows.landing_flow import get_landing_flow

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
    # PRIORIDAD 1: Detectar contexto de landing
    raw_text = context.memory.get("raw_text", "") if hasattr(context, "memory") else ""
    landing_flow = get_landing_flow()
    landing_response = landing_flow.process(raw_text)
    if landing_response:
        return landing_response

    # PRIORIDAD 2: Routing normal por intent
    handler = ROUTES.get(intent)
    if handler:
        return handler(context)
    return {
        "type": "text",
        "content": "No pude identificar la solicitud."
    }

from .flows import books, consultation, escalation, greeting, help, status, caregiver, property, receipt, card, chapter, calculator
from .flows.landing_flow import get_landing_flow
from .flows.calculator import get_calculator_flow

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
    "calculator": calculator.handle,
}


def dispatch(intent, context):
    raw_text = context.memory.get("raw_text", "") if hasattr(context, "memory") else ""
    session_id = context.session_id if hasattr(context, "session_id") else "default"
    
    # PRIORIDAD 0: Si hay sesión de calculadora activa, seguir ahí
    calc_flow = get_calculator_flow()
    if session_id in calc_flow.sessions:
        return calculator.handle(context)
    
    # PRIORIDAD 0.5: Si el intent es calculator, ir directo
    if intent == "calculator":
        handler = ROUTES.get("calculator")
        if handler:
            return handler(context)
    
    # PRIORIDAD 1: Detectar contexto de landing
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

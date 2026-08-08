from .models import Intent


INTENTS = [
    Intent("greeting", "Saludo"),
    Intent("help", "Solicitud de ayuda o menú"),
    Intent("status", "Consulta de estado del sistema"),
    Intent("book_interest", "Interés por libros"),
    Intent("receipt_registration", "Registro de ticket/comprobante"),
    Intent("card_trust", "Confianza tarjeta HEREDITARIA"),
    Intent("consultation_request", "Solicitud de consulta"),
    Intent("caregiver_problem", "Problema relacionado con cuidado"),
    Intent("property_question", "Consulta patrimonial"),
    Intent("elderly_support", "Apoyo adulto mayor"),
    Intent("general_information", "Información general"),
    Intent("human_escalation", "Solicitar atención humana"),
    Intent("unknown", "No identificado"),
]


def list_intents():
    return INTENTS

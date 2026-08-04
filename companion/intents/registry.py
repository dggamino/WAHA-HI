from .models import Intent


INTENTS = [
    Intent("book_interest", "Interés por libros"),
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

import re
import unicodedata


def _strip_accents(text):
    normalized = unicodedata.normalize("NFD", text)
    return "".join(c for c in normalized if unicodedata.category(c) != "Mn")


def classify(message):
    text = _strip_accents(message.lower())

    if re.search(r'\bcapitulo\s*\d+\b', text):
        return "chapter_request"

    saludos = ["hola", "buenos dias", "buenas tardes", "buenas noches",
               "buen dia", "que tal", "hey", "quien eres"]
    if any(s in text for s in saludos):
        return "greeting"

    ayuda = ["ayuda", "help", "menu", "opciones", "que puedes hacer",
             "info", "informacion"]
    if any(a in text for a in ayuda):
        return "help"

    if "status" in text or "estado del sistema" in text or "estas activo" in text:
        return "status"

    if "libro" in text or "libros" in text:
        return "book_interest"

    # ─── CALCULADORA GASTO INVISIBLE ─────────────────────────
    calc_keywords = [
        "calcula", "calcular", "gasto invisible", "estado de cuenta",
        "cuanto he gastado", "cuanto he regalado", "meses cuidando",
        "gasto bimestral", "cuanto gaste", "cuanto pague"
    ]
    if any(k in text for k in calc_keywords):
        return "calculator"
    # ─────────────────────────────────────────────────────────

    if "cuidado" in text or "cuidador" in text or "adulto mayor" in text or "enfermo" in text:
        return "caregiver_problem"

    if "patrimonio" in text or "herencia" in text or "testamento" in text or "casa" in text or "propiedad" in text:
        return "property_question"

    if "qr" in text or "ocr" in text or "ticket" in text or "registro" in text:
        return "receipt_registration"

    if "tarjeta" in text or "nfc" in text or "farmacia" in text or "tranquilidad" in text:
        return "card_trust"

    if "asesoria" in text or "consulta" in text:
        return "consultation_request"

    if "humano" in text or "persona" in text:
        return "human_escalation"

    return "unknown"

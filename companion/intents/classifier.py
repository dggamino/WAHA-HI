import unicodedata


def _strip_accents(text):
    normalized = unicodedata.normalize("NFD", text)
    return "".join(c for c in normalized if unicodedata.category(c) != "Mn")


def classify(message):

    text = _strip_accents(message.lower())

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

    # ─── NUEVOS INTENTS ──────────────────────────────────────
    if "cuidado" in text or "cuidador" in text or "adulto mayor" in text or "enfermo" in text:
        return "caregiver_problem"

    if "patrimonio" in text or "herencia" in text or "testamento" in text or "casa" in text or "propiedad" in text:
        return "property_question"
    # ─────────────────────────────────────────────────────────

    if "asesoria" in text or "consulta" in text:
        return "consultation_request"

    if "humano" in text or "persona" in text:
        return "human_escalation"

    return "unknown"

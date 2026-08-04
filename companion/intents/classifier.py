def classify(message):

    text = message.lower()

    if "libro" in text or "libros" in text:
        return "book_interest"

    if "asesoría" in text or "consulta" in text:
        return "consultation_request"

    if "humano" in text or "persona" in text:
        return "human_escalation"

    return "unknown"

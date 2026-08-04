"""
Intent Classifier Foundation v0.1.0
"""

def classify(message: str):
    text = message.lower()

    if "libro" in text or "libros" in text:
        return "book_interest"

    return "general_info"

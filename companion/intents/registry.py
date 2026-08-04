"""
Intent Registry Foundation v0.1.0
"""

INTENTS = {
    "book_interest": {
        "description": "Usuario interesado en libros HEREDITARIA"
    },
    "general_info": {
        "description": "Consulta general"
    }
}


def list_intents():
    return list(INTENTS.keys())


def get_intent(name):
    return INTENTS.get(name)

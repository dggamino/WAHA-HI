"""
Companion Intent Router Foundation v0.1.0
"""

from .intents.registry import get_intent


def dispatch(intent_name, context=None):
    intent = get_intent(intent_name)

    if not intent:
        return {
            "status": "unknown_intent",
            "intent": intent_name
        }

    return {
        "status": "routed",
        "intent": intent_name,
        "context": context
    }

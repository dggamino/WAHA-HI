"""
Responder Registry Foundation v0.1.0
"""

from .text import TextResponder

RESPONDERS = {
    "text": TextResponder()
}


def get_responder(name="text"):
    return RESPONDERS.get(name)

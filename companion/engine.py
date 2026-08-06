import logging
from pathlib import Path

from .session import Session
from .context import ConversationContext
from .router import dispatch
from .intents.classifier import classify
from .intents.registry import list_intents


logging.basicConfig(
    filename="/data/data/com.termux/files/home/WAHA-HI/logs/companion.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)


def load_prompts():

    prompt_path = Path("companion/prompts")

    prompts = list(prompt_path.glob("*.md"))

    logging.info(
        "PROMPTS_LOADED %s",
        len(prompts)
    )

    return prompts


def process(message, session_id=None, user_id=None):

    session = Session(
        session_id=session_id,
        channel="whatsapp"
    )

    intent = classify(message)

    # FIX: Usar ConversationContext según tu dataclass local
    context = ConversationContext(
        session_id=session.id,
        user_id=user_id or "",
        intent=intent
    )

    response = dispatch(
        intent,
        context
    )

    return response


def main():

    logging.info("COMPANION_STARTED")

    session = Session(
        channel="demo"
    )

    logging.info(
        "SESSION_CREATED %s",
        session.id
    )

    load_prompts()

    intents = list_intents()

    logging.info(
        "INTENTS_REGISTERED %s",
        len(intents)
    )

    result = process(
        "Quiero conocer los libros HEREDITARIA",
        session.id
    )

    logging.info(
        "ROUTER_READY %s",
        result
    )

    print(result)


if __name__ == "__main__":
    main()

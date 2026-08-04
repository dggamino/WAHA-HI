from dataclasses import dataclass


@dataclass
class WebhookEvent:

    event: str
    sender: str
    text: str
    session: str = "default"

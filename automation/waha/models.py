from dataclasses import dataclass


@dataclass
class IncomingMessage:

    session_id: str
    sender: str
    text: str
    channel: str = "whatsapp"



@dataclass
class OutgoingMessage:

    recipient: str
    text: str
    channel: str = "whatsapp"

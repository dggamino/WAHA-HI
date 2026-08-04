from dataclasses import dataclass


@dataclass
class SecurityContext:

    source: str
    authenticated: bool
    role: str = ""

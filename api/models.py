from dataclasses import dataclass


@dataclass
class APIRequest:

    action: str
    payload: dict



@dataclass
class APIResponse:

    status: str
    data: dict

from dataclasses import dataclass


@dataclass
class KnowledgeItem:

    id: str
    title: str
    content: str
    category: str

from dataclasses import dataclass, asdict


@dataclass
class AnalyticsReport:

    total_events: int
    messages_received: int
    intents_detected: int
    flows_executed: int
    leads_created: int


    def serialize(self):

        return asdict(self)

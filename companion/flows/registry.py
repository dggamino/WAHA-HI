"""
Flow Registry Foundation v0.1.0
"""

FLOWS = {}


def register_flow(intent, flow):
    FLOWS[intent] = flow


def get_flow(intent):
    return FLOWS.get(intent)


def list_flows():
    return list(FLOWS.keys())

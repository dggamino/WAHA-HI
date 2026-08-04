"""
Flow Base Foundation v0.1.0
"""

class BaseFlow:

    name = "base"

    def execute(self, context):
        raise NotImplementedError

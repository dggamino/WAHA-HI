"""
Metric definitions.
"""


class Metrics:


    def __init__(self):

        self.data = {

            "messages_received": 0,

            "intents_detected": 0,

            "flows_executed": 0,

            "prospects_created": 0,

            "responses_generated": 0

        }



    def increment(self, metric):

        if metric in self.data:

            self.data[metric] += 1



    def snapshot(self):

        return self.data

"""
System health collector.
"""


from orchestrator.registry import list_modules
from orchestrator.health import check_module



class HealthMonitor:


    def check(self):

        result = {}


        for name, module in list_modules().items():

            result[name] = check_module(
                module
            )


        return result

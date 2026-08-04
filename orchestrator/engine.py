import logging

from orchestrator.registry import list_modules
from orchestrator.health import check_module


logging.basicConfig(

    filename="logs/orchestrator.log",

    level=logging.INFO,

    format="%(asctime)s %(levelname)s %(message)s"

)



class Orchestrator:


    def __init__(self):

        self.modules = list_modules()



    def boot(self):

        results = []


        logging.info(
            "ORCHESTRATOR_STARTED"
        )


        for name, path in self.modules.items():

            result = check_module(path)

            results.append(result)


            logging.info(
                "%s %s",
                name,
                result["status"]
            )


        return results



def main():

    system = Orchestrator()

    results = system.boot()


    print(
        "WAHA-HI SYSTEM STATUS"
    )


    for result in results:

        print(result)



if __name__ == "__main__":

    main()

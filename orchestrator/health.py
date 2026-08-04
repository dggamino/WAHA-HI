import importlib


def check_module(path):

    try:

        importlib.import_module(path)

        return {
            "module": path,
            "status": "OK"
        }


    except Exception as error:

        return {
            "module": path,
            "status": "ERROR",
            "error": str(error)
        }

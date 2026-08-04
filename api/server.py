"""
API Gateway facade.

Future:
FastAPI / Flask implementation.
"""


from api.models import APIRequest
from api.router import APIRouter



class APIServer:


    def __init__(self):

        self.router = APIRouter()



    def handle(
        self,
        action,
        payload
    ):

        request = APIRequest(

            action,

            payload

        )


        return self.router.execute(
            request
        )

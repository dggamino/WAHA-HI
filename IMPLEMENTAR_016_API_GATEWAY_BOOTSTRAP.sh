#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "=== IMPLEMENTAR 016 — API Gateway Foundation v0.1.0 ==="

mkdir -p api


touch api/__init__.py


cat > api/__init__.py <<'EOF'
"""
WAHA-HI API Gateway Layer
"""
EOF


cat > api/models.py <<'EOF'
from dataclasses import dataclass


@dataclass
class APIRequest:

    action: str
    payload: dict



@dataclass
class APIResponse:

    status: str
    data: dict
EOF


cat > api/router.py <<'EOF'
"""
Internal API Router.
"""


from dashboard.service import DashboardService
from pipeline.full_runtime import FullPipeline



class APIRouter:


    def __init__(self):

        self.pipeline = FullPipeline()

        self.dashboard = DashboardService()



    def execute(self, request):


        if request.action == "message":


            result = self.pipeline.process(

                request.payload.get(
                    "text",
                    ""
                ),

                request.payload.get(
                    "phone",
                    "unknown"
                )

            )


            return {

                "status":
                "success",

                "response":
                result

            }



        if request.action == "dashboard":


            return {

                "status":
                "success",

                "dashboard":
                self.dashboard.snapshot()

            }



        return {

            "status":
            "error",

            "message":
            "unknown_action"

        }
EOF


cat > api/server.py <<'EOF'
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
EOF


cat > api/README.md <<'EOF'
# API Gateway Foundation

Capa de entrada externa.

Acciones iniciales:

- message
- dashboard

Futuro:

- REST API
- Webhooks WAHA
- Aplicaciones externas
EOF


echo ""
echo "=== VALIDACION API GATEWAY ==="

python3 - <<'EOF'

from api.server import APIServer


server = APIServer()


response = server.handle(

    "message",

    {

        "text":
        "Quiero conocer los libros HEREDITARIA",

        "phone":
        "5210000000000"

    }

)


print(response)

EOF


echo ""
echo "=== IMPLEMENTAR 016 COMPLETADO ==="

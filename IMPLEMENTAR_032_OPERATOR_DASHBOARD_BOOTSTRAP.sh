#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "=== IMPLEMENTAR 032 — Operator Dashboard Foundation v0.1.0 ==="


mkdir -p dashboard


touch dashboard/__init__.py


cat > dashboard/__init__.py <<'EOF'
"""
Operator Dashboard Layer
"""
EOF


cat > dashboard/view.py <<'EOF'
"""
Dashboard presentation layer.
"""


class DashboardView:


    def render(self, metrics):

        return {

            "dashboard":

            {

                "total_events":
                metrics.get(
                    "total_events",
                    0
                ),

                "messages":
                metrics.get(
                    "messages_received",
                    0
                ),

                "intents":
                metrics.get(
                    "intents_detected",
                    0
                ),

                "flows":
                metrics.get(
                    "flows_executed",
                    0
                ),

                "leads":
                metrics.get(
                    "leads_created",
                    0
                )

            }

        }
EOF


cat > dashboard/service.py <<'EOF'
from api.metrics.router import MetricsRouter
from dashboard.view import DashboardView



class DashboardService:


    def __init__(self):

        self.metrics = MetricsRouter()

        self.view = DashboardView()



    def status(self):

        response = self.metrics.get_metrics()


        return self.view.render(

            response["metrics"]

        )
EOF


cat > dashboard/README.md <<'EOF'
# Operator Dashboard Foundation

Consume:

Metrics API

Presenta:

- eventos
- mensajes
- intents
- flujos
- leads

No contiene lógica de dominio.
EOF


echo ""
echo "=== VALIDACION DASHBOARD ==="

python3 - <<'EOF'

from dashboard.service import DashboardService


dashboard = DashboardService()


print(
    dashboard.status()
)

EOF


echo ""
echo "=== IMPLEMENTAR 032 COMPLETADO ==="

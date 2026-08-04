#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "=== IMPLEMENTAR 015 — Dashboard Operational View Foundation v0.1.0 ==="

mkdir -p dashboard


touch dashboard/__init__.py


cat > dashboard/__init__.py <<'EOF'
"""
Operational Dashboard Layer
"""
EOF


cat > dashboard/service.py <<'EOF'
"""
Dashboard aggregation service.
"""


from orchestrator.registry import list_modules
from analytics.service import AnalyticsService
from ledger.service import LedgerService



class DashboardService:


    def __init__(self):

        self.analytics = AnalyticsService()

        self.ledger = LedgerService()



    def health(self):

        return {

            "modules":
            list_modules()

        }



    def metrics(self):

        return self.analytics.report()



    def events(self, limit=5):

        history = self.ledger.history()

        return history[-limit:]



    def snapshot(self):

        return {

            "health":
            self.health(),

            "metrics":
            self.metrics(),

            "recent_events":
            self.events()

        }
EOF


cat > dashboard/cli.py <<'EOF'
"""
CLI Dashboard
"""


from dashboard.service import DashboardService



def main():

    dashboard = DashboardService()


    report = dashboard.snapshot()


    print(
        "=== WAHA-HI OPERATIONAL DASHBOARD ==="
    )


    print("")

    print(
        "MODULES:"
    )

    print(
        report["health"]
    )


    print("")

    print(
        "METRICS:"
    )

    print(
        report["metrics"]
    )


    print("")

    print(
        "RECENT EVENTS:"
    )


    for event in report["recent_events"]:

        print(event)



if __name__ == "__main__":

    main()
EOF


cat > dashboard/README.md <<'EOF'
# Dashboard Operational View

Vista agregada del sistema.

Fuentes:

- Orchestrator
- Analytics
- Ledger

Futuro:

- API REST
- Panel web
- Métricas visuales
EOF


echo ""
echo "=== VALIDACION DASHBOARD ==="

python3 -m dashboard.cli


echo ""
echo "=== IMPLEMENTAR 015 COMPLETADO ==="

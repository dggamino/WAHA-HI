#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "=== IMPLEMENTAR 031 — Dashboard Metrics API Foundation v0.1.0 ==="


mkdir -p api/metrics


touch api/__init__.py
touch api/metrics/__init__.py


cat > api/metrics/service.py <<'EOF'
from ledger.service import LedgerService
from analytics.service import AnalyticsService


class MetricsService:


    def __init__(self):

        self.ledger = LedgerService()

        self.analytics = AnalyticsService()



    def current(self):

        events = list(
            self.ledger.history()
        )

        report = self.analytics.generate(
            events
        )

        return report.serialize()
EOF


cat > api/metrics/router.py <<'EOF'
from api.metrics.service import MetricsService



class MetricsRouter:


    def __init__(self):

        self.service = MetricsService()



    def get_metrics(self):

        return {

            "status": "success",

            "metrics":
                self.service.current()

        }
EOF


cat > api/metrics/README.md <<'EOF'
# Metrics API Foundation

Expone métricas operativas.

Fuente:

Ledger + Analytics

Salida:

Metrics JSON
EOF


echo ""
echo "=== VALIDACION METRICS API ==="

python3 - <<'EOF'

from api.metrics.router import MetricsRouter


router = MetricsRouter()


response = router.get_metrics()


print(response)

EOF


echo ""
echo "=== IMPLEMENTAR 031 COMPLETADO ==="

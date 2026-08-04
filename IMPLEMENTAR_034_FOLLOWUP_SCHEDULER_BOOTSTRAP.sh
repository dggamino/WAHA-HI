#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "=== IMPLEMENTAR 034 — Notification & Follow-up Scheduler Foundation v0.1.0 ==="

mkdir -p scheduler


touch scheduler/__init__.py


cat > scheduler/__init__.py <<'EOF'
"""
Follow-up Scheduler Layer
"""
EOF


cat > scheduler/models.py <<'EOF'
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class FollowUpTask:

    task_id: str
    prospect_id: str
    action: str
    status: str
    scheduled_at: str


    def serialize(self):

        return asdict(self)
EOF


cat > scheduler/repository.py <<'EOF'
import json
import os


FILE = "data/followups.json"


class TaskRepository:


    def __init__(self):

        os.makedirs(
            "data",
            exist_ok=True
        )

        if not os.path.exists(FILE):

            self.save_all([])



    def save_all(self, tasks):

        with open(FILE, "w") as f:

            json.dump(
                tasks,
                f,
                indent=2
            )



    def all(self):

        try:

            with open(FILE) as f:

                return json.load(f)

        except:

            return []



    def save(self, task):

        tasks = self.all()

        tasks.append(
            task.serialize()
        )

        self.save_all(tasks)

        return task
EOF


cat > scheduler/service.py <<'EOF'
import uuid
from datetime import datetime, timedelta

from scheduler.models import FollowUpTask
from scheduler.repository import TaskRepository



class FollowUpScheduler:


    def __init__(self):

        self.repository = TaskRepository()



    def schedule(

        self,

        prospect_id,

        action,

        delay_hours=24

    ):


        task = FollowUpTask(

            task_id=str(
                uuid.uuid4()
            ),

            prospect_id=prospect_id,

            action=action,

            status="pending",

            scheduled_at=(

                datetime.now()

                +

                timedelta(
                    hours=delay_hours
                )

            ).isoformat()

        )


        return self.repository.save(
            task
        )
EOF


cat > scheduler/adapter.py <<'EOF'
"""
Notification adapter boundary.

Future:

WAHA
Email
SMS
"""


class NotificationAdapter:


    def send(self, task):

        return {

            "task_id":
            task.task_id,

            "status":
            "queued"

        }
EOF


cat > scheduler/README.md <<'EOF'
# Follow-up Scheduler

Genera tareas posteriores a eventos.

Estados:

pending
queued
completed

No envía directamente mensajes.
EOF


echo ""
echo "=== VALIDACION FOLLOW-UP SCHEDULER ==="

python3 - <<'EOF'

from scheduler.service import FollowUpScheduler


scheduler = FollowUpScheduler()


task = scheduler.schedule(

    "5936fcf1-6a1a-4b8e-90bc-6ed4dc2d6c50",

    "schedule_contact"

)


print(
    task.serialize()
)

EOF


echo ""
echo "=== IMPLEMENTAR 034 COMPLETADO ==="

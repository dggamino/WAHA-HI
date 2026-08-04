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

import uuid
from datetime import datetime

from notifications.models import NotificationTask
from notifications.repository import NotificationRepository



class NotificationQueue:


    def __init__(self):

        self.repository = NotificationRepository()



    def enqueue(

        self,

        task_id,

        recipient,

        content,

        channel="whatsapp"

    ):


        notification = NotificationTask(

            notification_id=str(
                uuid.uuid4()
            ),

            task_id=task_id,

            channel=channel,

            recipient=recipient,

            content=content,

            status="queued",

            attempts=0,

            created_at=datetime.now().isoformat()

        )


        return self.repository.save(
            notification
        )

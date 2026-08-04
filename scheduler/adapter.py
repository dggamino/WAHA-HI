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

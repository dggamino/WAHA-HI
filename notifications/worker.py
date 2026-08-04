class DeliveryWorker:


    def process(self, notification):

        return {

            "notification_id":
            notification.notification_id,

            "status":
            "ready_for_delivery"

        }

from analytics.models import AnalyticsReport


class AnalyticsCollector:


    def collect(self, events):

        metrics = {

            "total_events": len(events),

            "messages_received": 0,

            "intents_detected": 0,

            "flows_executed": 0,

            "leads_created": 0

        }


        for event in events:


            if isinstance(event, tuple):

                event_type = event[1]

            else:

                event_type = event.event_type



            if event_type == "MESSAGE_RECEIVED":

                metrics[
                    "messages_received"
                ] += 1



            elif event_type == "INTENT_DETECTED":

                metrics[
                    "intents_detected"
                ] += 1



            elif event_type == "FLOW_EXECUTED":

                metrics[
                    "flows_executed"
                ] += 1



            elif event_type == "CRM_PROSPECT_CREATED":

                metrics[
                    "leads_created"
                ] += 1



        return AnalyticsReport(
            **metrics
        )

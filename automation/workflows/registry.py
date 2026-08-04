"""
Workflow registry.
"""


WORKFLOWS = {

    "CRM_PROSPECT_CREATED":
    {

        "workflow":
        "lead_followup",

        "action":
        "schedule_contact"

    }

}



def get_workflow(event_type):

    return WORKFLOWS.get(
        event_type
    )

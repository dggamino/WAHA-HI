"""
Lead qualification engine.
"""


from qualification.models import LeadProfile
from qualification.rules import evaluate



class QualificationEngine:


    def qualify(
        self,
        user_id,
        intent,
        source="conversation"
    ):


        level = evaluate(
            intent
        )


        return LeadProfile(

            user_id=user_id,

            intent=intent,

            interest_level=level,

            source=source

        )

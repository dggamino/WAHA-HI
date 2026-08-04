"""
Authentication guard.
"""


from security.config import validate_key
from security.models import SecurityContext



class SecurityGuard:


    def authenticate(self, api_key):

        role = validate_key(
            api_key
        )


        if role:

            return SecurityContext(

                source="api",

                authenticated=True,

                role=role

            )


        return SecurityContext(

            source="unknown",

            authenticated=False

        )

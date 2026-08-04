"""
Security middleware layer.
"""


from security.guard import SecurityGuard



class SecurityMiddleware:


    def __init__(self):

        self.guard = SecurityGuard()



    def protect(
        self,
        api_key
    ):

        context = self.guard.authenticate(
            api_key
        )


        if not context.authenticated:

            return {

                "status":
                "unauthorized"

            }


        return {

            "status":
            "authorized",

            "role":
            context.role

        }

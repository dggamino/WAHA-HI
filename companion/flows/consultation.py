class ConsultationFlow:


    def execute(self, context):

        if hasattr(context, "update"):

            try:

                context.update(
                    "flow",
                    "consultation"
                )

            except TypeError:

                context.update(
                    {
                        "flow": "consultation"
                    }
                )


        return {

            "type": "text",

            "content":
            "Consulta HEREDITARIA registrada. Un especialista continuará la atención."

        }



def handle(context):

    return ConsultationFlow().execute(
        context
    )

class GreetingFlow:

    def execute(self, context):

        if hasattr(context, "update"):
            try:
                context.update("flow", "greeting")
            except TypeError:
                context.update({"flow": "greeting"})

        return {
            "type": "text",
            "content": (
                "Hola, soy el asistente de HEREDITARIA™ 🏠\n\n"
                "Te ayudo con temas de patrimonio familiar, cuidado de "
                "adultos mayores y sucesiones.\n\n"
                "Escribe *ayuda* para ver qué puedo hacer, o cuéntame "
                "directamente tu situación."
            )
        }


def handle(context):
    return GreetingFlow().execute(context)

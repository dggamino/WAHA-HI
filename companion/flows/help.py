class HelpFlow:

    def execute(self, context):

        if hasattr(context, "update"):
            try:
                context.update("flow", "help")
            except TypeError:
                context.update({"flow": "help"})

        return {
            "type": "text",
            "content": (
                "Esto es lo que puedo hacer:\n\n"
                "📚 *Libros* — Escribe \"libros\" para conocer la Serie HEREDITARIA™\n"
                "🩺 *Cuidado* — Cuéntame si cuidas a un familiar mayor\n"
                "🏠 *Patrimonio* — Preguntas sobre casas, herencias, testamento\n"
                "👤 *Hablar con alguien* — Escribe \"humano\" para atención personal\n\n"
                "También puedes preguntarme directamente, en tus palabras."
            )
        }


def handle(context):
    return HelpFlow().execute(context)

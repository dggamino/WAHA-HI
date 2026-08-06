class CaregiverFlow:

    def execute(self, context):

        if hasattr(context, "update"):
            try:
                context.update("flow", "caregiver")
            except TypeError:
                context.update({"flow": "caregiver"})

        return {
            "type": "text",
            "content": (
                "🩺 *Cuidado de adultos mayores*\n\n"
                "Entiendo que cuidar a un familiar mayor puede ser agotador. "
                "Aquí tienes recursos que pueden ayudarte:\n\n"
                "📖 *Libro del Cuidador* — Guía práctica para cuidadores familiares\n"
                "🏥 *Asesoría médica* — Escribe 'asesoria' para orientación\n"
                "👤 *Apoyo emocional* — Escribe 'humano' para hablar con alguien\n\n"
                "¿Qué necesitas hoy?"
            )
        }


def handle(context):
    return CaregiverFlow().execute(context)

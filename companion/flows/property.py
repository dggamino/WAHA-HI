class PropertyFlow:

    def execute(self, context):

        if hasattr(context, "update"):
            try:
                context.update("flow", "property")
            except TypeError:
                context.update({"flow": "property"})

        return {
            "type": "text",
            "content": (
                "🏠 *Patrimonio y herencias*\n\n"
                "Te ayudo con temas de:\n\n"
                "📜 *Testamento* — Cómo hacerlo, tipos, requisitos\n"
                "🏡 *Herencia* — Proceso de sucesión, división de bienes\n"
                "📖 *Libro del Patrimonio Invisible* — Protege tu legado familiar\n"
                "👤 *Asesoría legal* — Escribe 'asesoria' para consulta\n\n"
                "¿Sobre qué tema necesitas información?"
            )
        }


def handle(context):
    return PropertyFlow().execute(context)

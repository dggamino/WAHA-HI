class CardFlow:

    def execute(self, context):
        if hasattr(context, "update"):
            try:
                context.update("flow", "card")
            except TypeError:
                context.update({"flow": "card"})

        return {
            "type": "video",
            "media": "./assets/hereditaria-nfc.mp4",
            "content": (
                "Con la tarjeta HEREDITARIA todo está registrado.\n"
                "Mayor tranquilidad para ustedes y para tu familia.\n"
                "Escribe TARJETA para apartar la tuya."
            )
        }


def handle(context):
    return CardFlow().execute(context)

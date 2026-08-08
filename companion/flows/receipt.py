class ReceiptFlow:

    def execute(self, context):
        if hasattr(context, "update"):
            try:
                context.update("flow", "receipt")
            except TypeError:
                context.update({"flow": "receipt"})

        return {
            "type": "video",
            "media": "./assets/hereditaria-qr.mp4",
            "content": (
                "No es un testamento. Es tu historial registrado.\n"
                "Foto al ticket → Check verde."
            )
        }


def handle(context):
    return ReceiptFlow().execute(context)

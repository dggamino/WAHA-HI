def handle(context):

    context.update("flow", "escalation")

    return {
        "type": "text",
        "content": "Solicitud enviada a atención humana."
    }

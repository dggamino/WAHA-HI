"""
Conversation Context Layer
"""
from .models import ConversationContext
from .service import ContextService
from .merge import ContextMerger

# Alias para compatibilidad
Context = ConversationContext

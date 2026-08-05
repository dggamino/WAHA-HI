"""
companion/actions/catalog.py

WAHA-HI Actions Catalog — Sprint 031

Responsabilidad:
  - Definir y registrar el catálogo de acciones built-in del sistema.
  - Proveer acciones fundamentales que el ActionPlanner puede invocar.
  - Cada acción está documentada, versionada y categorizada.

Diseño:
  - Cada acción es una función pura o con side-effects controlados.
  - Registro automático vía @register_action.
  - Acciones organizadas por dominio: core, memory, context, response.

Acciones incluidas:
  - core/noop: Acción nula (para testing y placeholders).
  - core/echo: Repite el input.
  - core/wait: Espera un tiempo determinado.
  - memory/store: Almacena un valor en memoria.
  - memory/recall: Recupera un valor de memoria.
  - context/get: Obtiene una clave del contexto.
  - context/set: Establece una clave en el contexto.
  - response/build: Construye una respuesta estructurada.
  - response/append: Agrega contenido a una respuesta acumulativa.

Compatibilidad:
  - 020–030 intactos.
  - No modifica pipeline.py ni FlowOrchestrator.
"""

from __future__ import annotations

import time
from typing import Any, Dict, List, Optional

from companion.action_registry import register_action


# ═══════════════════════════════════════════════════════════════
# ACCIONES CORE
# ═══════════════════════════════════════════════════════════════

@register_action(
    name="core/noop",
    description="Acción nula. No realiza operación. Útil para testing y placeholders.",
    version="0.1.0",
    tags=["core", "system"],
)
def core_noop() -> None:
    """No-op. Retorna None."""
    return None


@register_action(
    name="core/echo",
    description="Repite el mensaje de entrada. Útil para validación de pipelines.",
    version="0.1.0",
    tags=["core", "debug"],
)
def core_echo(message: str) -> str:
    """Retorna el mensaje sin modificar."""
    return message


@register_action(
    name="core/wait",
    description="Espera un tiempo determinado en segundos.",
    version="0.1.0",
    tags=["core", "system"],
)
def core_wait(seconds: float = 0.1) -> Dict[str, Any]:
    """Espera el tiempo especificado y retorna metadata."""
    start = time.time()
    time.sleep(seconds)
    elapsed = time.time() - start
    return {
        "requested_seconds": seconds,
        "actual_seconds": elapsed,
    }


@register_action(
    name="core/identity",
    description="Retorna el input sin modificar. Soporta cualquier tipo.",
    version="0.1.0",
    tags=["core", "transform"],
)
def core_identity(value: Any) -> Any:
    """Función identidad."""
    return value


@register_action(
    name="core/merge",
    description="Fusiona múltiples diccionarios en uno solo.",
    version="0.1.0",
    tags=["core", "transform"],
)
def core_merge(*, sources: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Fusiona una lista de diccionarios. Las claves posteriores sobrescriben."""
    result: Dict[str, Any] = {}
    for source in sources:
        result.update(source)
    return result


# ═══════════════════════════════════════════════════════════════
# ACCIONES DE MEMORIA
# ═══════════════════════════════════════════════════════════════

@register_action(
    name="memory/store",
    description="Almacena un par clave-valor en memoria persistente.",
    version="0.1.0",
    tags=["memory", "storage"],
    requires_memory=True,
)
def memory_store(key: str, value: Any, memory: Any) -> Dict[str, Any]:
    """
    Almacena un valor en memoria.
    
    Args:
        key: Clave de almacenamiento.
        value: Valor a almacenar.
        memory: Instancia de memoria (inyectada).
    
    Returns:
        Metadata de la operación.
    """
    # Interfaz flexible: soporta dict-like o métodos store/set
    if hasattr(memory, "store"):
        memory.store(key, value)
    elif hasattr(memory, "set"):
        memory.set(key, value)
    elif isinstance(memory, dict):
        memory[key] = value
    else:
        raise TypeError(f"Tipo de memoria no soportado: {type(memory)}")
    
    return {"key": key, "stored": True, "timestamp": time.time()}


@register_action(
    name="memory/recall",
    description="Recupera un valor de memoria persistente por clave.",
    version="0.1.0",
    tags=["memory", "retrieval"],
    requires_memory=True,
)
def memory_recall(key: str, memory: Any, default: Any = None) -> Any:
    """
    Recupera un valor de memoria.
    
    Args:
        key: Clave a recuperar.
        memory: Instancia de memoria (inyectada).
        default: Valor por defecto si la clave no existe.
    
    Returns:
        El valor almacenado o default.
    """
    if hasattr(memory, "recall"):
        return memory.recall(key, default)
    elif hasattr(memory, "get"):
        return memory.get(key, default)
    elif isinstance(memory, dict):
        return memory.get(key, default)
    else:
        raise TypeError(f"Tipo de memoria no soportado: {type(memory)}")


@register_action(
    name="memory/list_keys",
    description="Lista todas las claves disponibles en memoria.",
    version="0.1.0",
    tags=["memory", "introspection"],
    requires_memory=True,
)
def memory_list_keys(memory: Any) -> List[str]:
    """Lista las claves disponibles en memoria."""
    if hasattr(memory, "list_keys"):
        return memory.list_keys()
    elif hasattr(memory, "keys"):
        return list(memory.keys())
    elif isinstance(memory, dict):
        return list(memory.keys())
    else:
        raise TypeError(f"Tipo de memoria no soportado: {type(memory)}")


# ═══════════════════════════════════════════════════════════════
# ACCIONES DE CONTEXTO
# ═══════════════════════════════════════════════════════════════

@register_action(
    name="context/get",
    description="Obtiene un valor del contexto de sesión por clave.",
    version="0.1.0",
    tags=["context", "retrieval"],
    requires_context=True,
)
def context_get(key: str, ctx: Any, default: Any = None) -> Any:
    """
    Obtiene un valor del contexto.
    
    Args:
        key: Clave en el contexto.
        ctx: Contexto de sesión (inyectado).
        default: Valor por defecto.
    
    Returns:
        Valor del contexto o default.
    """
    if hasattr(ctx, "get"):
        return ctx.get(key, default)
    elif isinstance(ctx, dict):
        return ctx.get(key, default)
    else:
        raise TypeError(f"Tipo de contexto no soportado: {type(ctx)}")


@register_action(
    name="context/set",
    description="Establece un valor en el contexto de sesión.",
    version="0.1.0",
    tags=["context", "storage"],
    requires_context=True,
)
def context_set(key: str, value: Any, ctx: Any) -> Dict[str, Any]:
    """
    Establece un valor en el contexto.
    
    Args:
        key: Clave a establecer.
        value: Valor a asignar.
        ctx: Contexto de sesión (inyectado).
    
    Returns:
        Metadata de la operación.
    """
    if hasattr(ctx, "set"):
        ctx.set(key, value)
    elif isinstance(ctx, dict):
        ctx[key] = value
    else:
        raise TypeError(f"Tipo de contexto no soportado: {type(ctx)}")
    
    return {"key": key, "set": True, "timestamp": time.time()}


@register_action(
    name="context/get_all",
    description="Obtiene todo el contexto de sesión como diccionario.",
    version="0.1.0",
    tags=["context", "introspection"],
    requires_context=True,
)
def context_get_all(ctx: Any) -> Dict[str, Any]:
    """Retorna el contexto completo."""
    if hasattr(ctx, "to_dict"):
        return ctx.to_dict()
    elif isinstance(ctx, dict):
        return dict(ctx)
    else:
        return {"raw": str(ctx)}


# ═══════════════════════════════════════════════════════════════
# ACCIONES DE RESPUESTA
# ═══════════════════════════════════════════════════════════════

@register_action(
    name="response/build",
    description="Construye una respuesta estructurada con texto, metadata y sugerencias.",
    version="0.1.0",
    tags=["response", "builder"],
)
def response_build(
    text: str,
    metadata: Optional[Dict[str, Any]] = None,
    suggestions: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Construye una respuesta estructurada.
    
    Args:
        text: Texto principal de la respuesta.
        metadata: Metadata adicional.
        suggestions: Lista de sugerencias de follow-up.
    
    Returns:
        Diccionario estructurado de respuesta.
    """
    return {
        "type": "response",
        "text": text,
        "metadata": metadata or {},
        "suggestions": suggestions or [],
        "timestamp": time.time(),
    }


@register_action(
    name="response/append",
    description="Agrega contenido a una respuesta acumulativa.",
    version="0.1.0",
    tags=["response", "builder"],
)
def response_append(
    current: Dict[str, Any],
    text: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Agrega contenido a una respuesta existente.
    
    Args:
        current: Respuesta actual.
        text: Texto a agregar.
        metadata: Metadata a fusionar.
    
    Returns:
        Respuesta actualizada.
    """
    result = dict(current)
    if text:
        existing = result.get("text", "")
        result["text"] = existing + "\n" + text if existing else text
    if metadata:
        existing_meta = result.get("metadata", {})
        existing_meta.update(metadata)
        result["metadata"] = existing_meta
    return result


@register_action(
    name="response/format",
    description="Formatea una respuesta con un template dado.",
    version="0.1.0",
    tags=["response", "transform"],
)
def response_format(template: str, **kwargs: Any) -> str:
    """
    Formatea un template con variables.
    
    Args:
        template: Template con placeholders {var}.
        **kwargs: Variables para interpolar.
    
    Returns:
        String formateado.
    """
    try:
        return template.format(**kwargs)
    except KeyError as e:
        raise ValueError(f"Variable faltante en template: {e}")


# ═══════════════════════════════════════════════════════════════
# UTILIDADES DEL CATÁLOGO
# ═══════════════════════════════════════════════════════════════

def get_catalog_actions() -> List[str]:
    """Retorna lista de nombres de acciones del catálogo built-in."""
    from companion.action_registry import get_default_registry
    reg = get_default_registry()
    return [name for name in reg.action_names if name.startswith(("core/", "memory/", "context/", "response/"))]


def list_catalog_actions() -> List[Dict[str, Any]]:
    """Retorna descripciones de todas las acciones del catálogo."""
    from companion.action_registry import get_default_registry
    reg = get_default_registry()
    actions = []
    for name in get_catalog_actions():
        try:
            action = reg.get(name)
            actions.append({
                "name": action.metadata.name,
                "description": action.metadata.description,
                "version": action.metadata.version,
                "tags": action.metadata.tags,
                "parameters": action.metadata.parameters,
                "requires_context": action.metadata.requires_context,
                "requires_memory": action.metadata.requires_memory,
            })
        except Exception:
            pass
    return actions


def describe_catalog_action(name: str) -> Optional[Dict[str, Any]]:
    """Describe una acción del catálogo por nombre."""
    from companion.action_registry import get_default_registry, ActionNotFoundError
    reg = get_default_registry()
    try:
        action = reg.get(name)
        return {
            "name": action.metadata.name,
            "description": action.metadata.description,
            "version": action.metadata.version,
            "tags": action.metadata.tags,
            "parameters": action.metadata.parameters,
            "returns": action.metadata.returns,
            "requires_context": action.metadata.requires_context,
            "requires_memory": action.metadata.requires_memory,
        }
    except ActionNotFoundError:
        return None

"""
companion/actions/__init__.py

WAHA-HI Actions Package — Sprint 031

Responsabilidad:
  - Punto de entrada del paquete de acciones.
  - Expone las acciones del catálogo y utilidades de contexto/memoria/respuesta.
  - Auto-registra acciones del catálogo al importar el paquete.

Diseño:
  - Importación lazy del catálogo para evitar circular dependencies.
  - Exports explícitos para type checkers y autocompletado.

Compatibilidad:
  - 020–030 intactos.
"""

from __future__ import annotations

# Importaciones del catálogo (se registran automáticamente al importar)
from companion.actions.catalog import (
    get_catalog_actions,
    list_catalog_actions,
    describe_catalog_action,
)

# Utilidades
from companion.actions.context import ActionContext
from companion.actions.memory import ActionMemory
from companion.actions.response import ActionResponseBuilder

__all__ = [
    # Catálogo
    "get_catalog_actions",
    "list_catalog_actions",
    "describe_catalog_action",
    # Utilidades
    "ActionContext",
    "ActionMemory",
    "ActionResponseBuilder",
]

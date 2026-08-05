"""
companion/actions/context.py

WAHA-HI ActionContext — Sprint 031

Responsabilidad:
  - Wrapper tipado y seguro para el contexto de sesión.
  - Abstrae la estructura interna del contexto.
  - Provee métodos de conveniencia para acciones que requieren contexto.

Diseño:
  - Fachada sobre dict o objeto de contexto existente.
  - Inmutable por defecto; mutaciones explícitas via métodos.
  - Compatible con cualquier objeto que soporte .get()/.set() o dict-like.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Iterator


class ActionContext:
    """
    Wrapper seguro para contexto de sesión.
    
    Permite a las acciones acceder al contexto sin conocer
    la implementación subyacente (Session, dict, etc.).
    """
    
    def __init__(self, source: Any):
        self._source = source
        self._overlay: Dict[str, Any] = {}
    
    def get(self, key: str, default: Any = None) -> Any:
        """Obtiene un valor del contexto."""
        if key in self._overlay:
            return self._overlay[key]
        if hasattr(self._source, "get"):
            return self._source.get(key, default)
        if isinstance(self._source, dict):
            return self._source.get(key, default)
        return default
    
    def set(self, key: str, value: Any) -> None:
        """Establece un valor en el overlay (no modifica el source)."""
        self._overlay[key] = value
    
    def has(self, key: str) -> bool:
        """Verifica si una clave existe."""
        return key in self._overlay or (
            hasattr(self._source, "__contains__") and key in self._source
        )
    
    def keys(self) -> Iterator[str]:
        """Itera sobre todas las claves disponibles."""
        seen = set(self._overlay.keys())
        for k in seen:
            yield k
        if hasattr(self._source, "keys"):
            for k in self._source.keys():
                if k not in seen:
                    yield k
        elif isinstance(self._source, dict):
            for k in self._source.keys():
                if k not in seen:
                    yield k
    
    def to_dict(self) -> Dict[str, Any]:
        """Retorna copia completa como diccionario."""
        result: Dict[str, Any] = {}
        if hasattr(self._source, "to_dict"):
            result.update(self._source.to_dict())
        elif isinstance(self._source, dict):
            result.update(self._source)
        else:
            result["_raw"] = str(self._source)
        result.update(self._overlay)
        return result
    
    def get_session_id(self) -> Optional[str]:
        """Conveniencia: retorna session_id si existe."""
        return self.get("session_id")
    
    def get_user_id(self) -> Optional[str]:
        """Conveniencia: retorna user_id si existe."""
        return self.get("user_id")
    
    def get_turn_count(self) -> int:
        """Conveniencia: retorna contador de turnos."""
        return self.get("turn_count", 0)
    
    def __repr__(self) -> str:
        return f"<ActionContext keys={list(self.keys())}>"

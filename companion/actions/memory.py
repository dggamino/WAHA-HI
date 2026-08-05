"""
companion/actions/memory.py

WAHA-HI ActionMemory — Sprint 031

Responsabilidad:
  - Wrapper tipado para acceso a memoria persistente.
  - Abstrae SemanticMemory, PersistentMemory, etc.
  - Provee interfaz uniforme para acciones.

Diseño:
  - Fachada sobre cualquier backend de memoria.
  - Soporte para operaciones CRUD básicas.
  - Namespace opcional para aislar acciones.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


class ActionMemory:
    """
    Wrapper seguro para memoria persistente.
    
    Unifica acceso a diferentes implementaciones de memoria
    (dict, SemanticMemory, PersistentMemory, etc.).
    """
    
    def __init__(self, source: Any, namespace: Optional[str] = None):
        self._source = source
        self._namespace = namespace
        self._local: Dict[str, Any] = {}
    
    def _namespaced_key(self, key: str) -> str:
        if self._namespace:
            return f"{self._namespace}:{key}"
        return key
    
    def store(self, key: str, value: Any) -> None:
        """Almacena un valor."""
        ns_key = self._namespaced_key(key)
        self._local[ns_key] = value
        if hasattr(self._source, "store"):
            self._source.store(ns_key, value)
        elif hasattr(self._source, "set"):
            self._source.set(ns_key, value)
        elif isinstance(self._source, dict):
            self._source[ns_key] = value
    
    def recall(self, key: str, default: Any = None) -> Any:
        """Recupera un valor."""
        ns_key = self._namespaced_key(key)
        if ns_key in self._local:
            return self._local[ns_key]
        if hasattr(self._source, "recall"):
            return self._source.recall(ns_key, default)
        if hasattr(self._source, "get"):
            return self._source.get(ns_key, default)
        if isinstance(self._source, dict):
            return self._source.get(ns_key, default)
        return default
    
    def has(self, key: str) -> bool:
        """Verifica si una clave existe."""
        ns_key = self._namespaced_key(key)
        if ns_key in self._local:
            return True
        if hasattr(self._source, "has"):
            return self._source.has(ns_key)
        if hasattr(self._source, "__contains__"):
            return ns_key in self._source
        return False
    
    def list_keys(self, prefix: Optional[str] = None) -> List[str]:
        """Lista claves, opcionalmente filtradas por prefijo."""
        keys: List[str] = []
        all_sources = [self._local]
        if isinstance(self._source, dict):
            all_sources.append(self._source)
        elif hasattr(self._source, "keys"):
            all_sources.append({k: None for k in self._source.keys()})
        
        for source in all_sources:
            for k in source:
                if prefix is None or k.startswith(prefix):
                    keys.append(k)
        return list(dict.fromkeys(keys))  # dedup preservando orden
    
    def delete(self, key: str) -> bool:
        """Elimina una clave. Retorna True si existía."""
        ns_key = self._namespaced_key(key)
        existed = False
        if ns_key in self._local:
            del self._local[ns_key]
            existed = True
        if hasattr(self._source, "delete"):
            existed = self._source.delete(ns_key) or existed
        elif isinstance(self._source, dict) and ns_key in self._source:
            del self._source[ns_key]
            existed = True
        return existed
    
    def clear_local(self) -> None:
        """Limpia solo el cache local, no el source."""
        self._local.clear()
    
    def __repr__(self) -> str:
        return f"<ActionMemory namespace={self._namespace} keys={len(self.list_keys())}>"

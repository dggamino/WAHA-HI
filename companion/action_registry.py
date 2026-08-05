"""
companion/action_registry.py

WAHA-HI Action Registry — Sprint 031

Responsabilidad:
  - Mantener un registro centralizado de acciones ejecutables.
  - Soportar registro dinámico y búsqueda por nombre.
  - Proveer validación de firmas y metadatos de acciones.
  - Ser thread-safe para entornos concurrentes.

Diseño:
  - Registry Pattern con decorador @register_action.
  - Cada acción es un callable con metadatos estandarizados.
  - El registro es un singleton por proceso.

Compatibilidad:
  - 020–030 intactos.
  - No modifica pipeline.py ni FlowOrchestrator.
"""

from __future__ import annotations

import inspect
import threading
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, TypeVar, Union


# ──────────────────────────────────────────────────────────────
# Tipos y constantes
# ──────────────────────────────────────────────────────────────

T = TypeVar("T")

DEFAULT_REGISTRY_NAME = "default"


class ActionRegistryError(Exception):
    """Base para errores del registro de acciones."""
    pass


class ActionNotFoundError(ActionRegistryError):
    """Acción no encontrada en el registro."""
    pass


class ActionValidationError(ActionRegistryError):
    """Firma o metadatos de acción inválidos."""
    pass


class DuplicateActionError(ActionRegistryError):
    """Intento de registrar una acción ya existente."""
    pass


# ──────────────────────────────────────────────────────────────
# ActionMetadata — descriptor de una acción registrada
# ──────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class ActionMetadata:
    """
    Metadatos inmutables de una acción ejecutable.
    
    Attributes:
        name: Identificador único de la acción.
        description: Descripción legible de la acción.
        version: Versión semántica de la acción.
        parameters: Lista de parámetros esperados (nombre, tipo, obligatorio).
        returns: Tipo de retorno esperado.
        tags: Etiquetas para categorización.
        requires_context: Si la acción requiere el contexto de sesión.
        requires_memory: Si la acción requiere acceso a memoria persistente.
    """
    name: str
    description: str = ""
    version: str = "0.1.0"
    parameters: List[Dict[str, Any]] = field(default_factory=list)
    returns: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    requires_context: bool = False
    requires_memory: bool = False


# ──────────────────────────────────────────────────────────────
# RegisteredAction — callable envuelto con metadatos
# ──────────────────────────────────────────────────────────────

class RegisteredAction:
    """
    Envoltura para una acción registrada.
    
    Expone:
      - metadata: ActionMetadata
      - callable: la función o método subyacente
      - execute(**kwargs): invocación validada
    """

    def __init__(
        self,
        name: str,
        callable_ref: Callable[..., Any],
        description: str = "",
        version: str = "0.1.0",
        tags: Optional[List[str]] = None,
        requires_context: bool = False,
        requires_memory: bool = False,
    ):
        self._callable = callable_ref
        self.metadata = ActionMetadata(
            name=name,
            description=description,
            version=version,
            parameters=self._extract_parameters(callable_ref),
            returns=self._extract_return_type(callable_ref),
            tags=tags or [],
            requires_context=requires_context,
            requires_memory=requires_memory,
        )

    @staticmethod
    def _extract_parameters(fn: Callable[..., Any]) -> List[Dict[str, Any]]:
        """Extrae parámetros de la firma de la función."""
        sig = inspect.signature(fn)
        params = []
        for pname, param in sig.parameters.items():
            if pname in ("ctx", "context", "memory"):
                # Parámetros inyectados por el executor, no por el planner
                continue
            params.append({
                "name": pname,
                "type": str(param.annotation) if param.annotation != inspect.Parameter.empty else "Any",
                "required": param.default == inspect.Parameter.empty,
                "default": param.default if param.default != inspect.Parameter.empty else None,
            })
        return params

    @staticmethod
    def _extract_return_type(fn: Callable[..., Any]) -> Optional[str]:
        """Extrae el tipo de retorno anotado."""
        sig = inspect.signature(fn)
        if sig.return_annotation != inspect.Parameter.empty:
            return str(sig.return_annotation)
        return None

    def execute(self, **kwargs: Any) -> Any:
        """Ejecuta la acción con los argumentos proporcionados."""
        return self._callable(**kwargs)

    def __call__(self, **kwargs: Any) -> Any:
        return self.execute(**kwargs)

    def __repr__(self) -> str:
        return f"<RegisteredAction {self.metadata.name} v{self.metadata.version}>"


# ──────────────────────────────────────────────────────────────
# ActionRegistry — registro centralizado
# ──────────────────────────────────────────────────────────────

class ActionRegistry:
    """
    Registro centralizado de acciones ejecutables.
    
    Thread-safe. Singleton por nombre de registro.
    """

    _instances: Dict[str, "ActionRegistry"] = {}
    _lock = threading.Lock()

    def __new__(cls, name: str = DEFAULT_REGISTRY_NAME) -> "ActionRegistry":
        with cls._lock:
            if name not in cls._instances:
                instance = super().__new__(cls)
                instance._init(name)
                cls._instances[name] = instance
            return cls._instances[name]

    def _init(self, name: str) -> None:
        self._name = name
        self._actions: Dict[str, RegisteredAction] = {}
        self._action_lock = threading.RLock()

    @property
    def name(self) -> str:
        return self._name

    @property
    def action_names(self) -> List[str]:
        """Lista de nombres de acciones registradas."""
        with self._action_lock:
            return list(self._actions.keys())

    @property
    def actions(self) -> Dict[str, RegisteredAction]:
        """Copia de las acciones registradas."""
        with self._action_lock:
            return dict(self._actions)

    def register(
        self,
        name: str,
        callable_ref: Callable[..., Any],
        description: str = "",
        version: str = "0.1.0",
        tags: Optional[List[str]] = None,
        requires_context: bool = False,
        requires_memory: bool = False,
        allow_override: bool = False,
    ) -> RegisteredAction:
        """
        Registra una acción en el registro.
        
        Args:
            name: Identificador único.
            callable_ref: Función o callable a registrar.
            description, version, tags: Metadatos.
            requires_context: Si necesita contexto de sesión.
            requires_memory: Si necesita acceso a memoria.
            allow_override: Si permite sobrescribir una acción existente.
        
        Returns:
            Instancia de RegisteredAction.
        
        Raises:
            DuplicateActionError: Si la acción ya existe y allow_override=False.
            ActionValidationError: Si el callable no es válido.
        """
        if not callable(callable_ref):
            raise ActionValidationError(
                f"El valor proporcionado para '{name}' no es callable."
            )

        with self._action_lock:
            if name in self._actions and not allow_override:
                raise DuplicateActionError(
                    f"La acción '{name}' ya está registrada. "
                    f"Use allow_override=True para sobrescribir."
                )

            action = RegisteredAction(
                name=name,
                callable_ref=callable_ref,
                description=description,
                version=version,
                tags=tags or [],
                requires_context=requires_context,
                requires_memory=requires_memory,
            )
            self._actions[name] = action
            return action

    def unregister(self, name: str) -> bool:
        """Elimina una acción del registro."""
        with self._action_lock:
            if name in self._actions:
                del self._actions[name]
                return True
            return False

    def get(self, name: str) -> RegisteredAction:
        """
        Recupera una acción por nombre.
        
        Raises:
            ActionNotFoundError: Si la acción no existe.
        """
        with self._action_lock:
            if name not in self._actions:
                raise ActionNotFoundError(f"Acción '{name}' no encontrada en el registro.")
            return self._actions[name]

    def has(self, name: str) -> bool:
        """Verifica si una acción está registrada."""
        with self._action_lock:
            return name in self._actions

    def find_by_tag(self, tag: str) -> List[RegisteredAction]:
        """Busca acciones por etiqueta."""
        with self._action_lock:
            return [
                action for action in self._actions.values()
                if tag in action.metadata.tags
            ]

    def find_by_prefix(self, prefix: str) -> List[RegisteredAction]:
        """Busca acciones cuyo nombre comience con el prefijo."""
        with self._action_lock:
            return [
                action for action in self._actions.values()
                if action.metadata.name.startswith(prefix)
            ]

    def clear(self) -> None:
        """Elimina todas las acciones del registro."""
        with self._action_lock:
            self._actions.clear()

    def validate_action_plan(self, plan: Dict[str, Any]) -> List[str]:
        """
        Valida un plan de acciones contra el registro.
        
        Args:
            plan: Diccionario con clave 'actions' que contiene lista de dicts
                  con 'name' y 'params'.
        
        Returns:
            Lista de errores encontrados. Vacía si todo es válido.
        """
        errors = []
        actions = plan.get("actions", [])
        if not isinstance(actions, list):
            return ["El plan debe contener una lista 'actions'."]

        for idx, action_def in enumerate(actions):
            action_name = action_def.get("name")
            if not action_name:
                errors.append(f"Acción #{idx}: falta 'name'.")
                continue
            if not self.has(action_name):
                errors.append(f"Acción #{idx}: '{action_name}' no está registrada.")
                continue
            # Validación básica de parámetros
            registered = self.get(action_name)
            required_params = {
                p["name"] for p in registered.metadata.parameters
                if p["required"]
            }
            provided_params = set(action_def.get("params", {}).keys())
            missing = required_params - provided_params
            if missing:
                errors.append(
                    f"Acción '{action_name}': faltan parámetros obligatorios: {missing}"
                )
        return errors

    def __len__(self) -> int:
        with self._action_lock:
            return len(self._actions)

    def __contains__(self, name: str) -> bool:
        return self.has(name)

    def __repr__(self) -> str:
        with self._action_lock:
            return (
                f"<ActionRegistry '{self._name}' "
                f"actions={len(self._actions)}>"
            )


# ──────────────────────────────────────────────────────────────
# Decorador @register_action
# ──────────────────────────────────────────────────────────────

def register_action(
    name: Optional[str] = None,
    description: str = "",
    version: str = "0.1.0",
    tags: Optional[List[str]] = None,
    requires_context: bool = False,
    requires_memory: bool = False,
    registry: Optional[ActionRegistry] = None,
    allow_override: bool = False,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorador para registrar una función como acción ejecutable.
    
    Uso:
        @register_action(name="greet", description="Saluda al usuario")
        def greet(name: str) -> str:
            return f"Hola, {name}"
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        action_name = name or func.__name__
        target_registry = registry or ActionRegistry()
        target_registry.register(
            name=action_name,
            callable_ref=func,
            description=description,
            version=version,
            tags=tags,
            requires_context=requires_context,
            requires_memory=requires_memory,
            allow_override=allow_override,
        )
        return func
    return decorator


# ──────────────────────────────────────────────────────────────
# Funciones de conveniencia
# ──────────────────────────────────────────────────────────────

def get_default_registry() -> ActionRegistry:
    """Retorna el registro por defecto."""
    return ActionRegistry(DEFAULT_REGISTRY_NAME)


def reset_registry(name: str = DEFAULT_REGISTRY_NAME) -> None:
    """Reinicia un registro (útil para tests)."""
    registry = ActionRegistry._instances.get(name)
    if registry:
        registry.clear()

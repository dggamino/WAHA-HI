"""
companion/action_executor.py

WAHA-HI Action Executor — Sprint 031

Responsabilidad:
  - Ejecutar planes de acciones generados por ActionPlanner.
  - Inyectar dependencias (contexto, memoria) cuando las acciones lo requieren.
  - Capturar resultados, errores y métricas de ejecución.
  - Integrar con ExecutionTracker para trazabilidad.
  - Retornar resultados estructurados que el Pipeline puede consumir.

Diseño:
  - Command Pattern adaptado: el Executor es el Invoker.
  - Cada ejecución produce un ActionResult con estado, salida y metadata.
  - Soporte para ejecución secuencial y (preparado para) paralela.
  - Inyección de dependencias por reflexión de firma.

Compatibilidad:
  - 020–030 intactos.
  - No modifica pipeline.py ni FlowOrchestrator.
  - Se inserta entre Adaptive Action Planner y Execution Tracker.
"""

from __future__ import annotations

import time
import traceback
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from companion.action_registry import (
    ActionRegistry,
    ActionNotFoundError,
    get_default_registry,
)


# ──────────────────────────────────────────────────────────────
# Tipos de estado de ejecución
# ──────────────────────────────────────────────────────────────

class ExecutionStatus(str, Enum):
    """Estados posibles de una ejecución de acción."""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"
    TIMEOUT = "timeout"


# ──────────────────────────────────────────────────────────────
# ActionResult — resultado de una ejecución
# ──────────────────────────────────────────────────────────────

@dataclass
class ActionResult:
    """
    Resultado inmutable de la ejecución de una acción.
    
    Attributes:
        action_name: Nombre de la acción ejecutada.
        status: Estado final de la ejecución.
        output: Valor retornado por la acción (si success).
        error: Mensaje de error (si failed).
        traceback: Traza completa del error (si failed).
        duration_ms: Duración de la ejecución en milisegundos.
        timestamp: Timestamp de inicio (epoch).
        metadata: Metadatos adicionales de la ejecución.
    """
    action_name: str
    status: ExecutionStatus
    output: Any = None
    error: Optional[str] = None
    traceback: Optional[str] = None
    duration_ms: float = 0.0
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def is_success(self) -> bool:
        return self.status == ExecutionStatus.SUCCESS

    @property
    def is_failure(self) -> bool:
        return self.status in (ExecutionStatus.FAILED, ExecutionStatus.TIMEOUT)

    def to_dict(self) -> Dict[str, Any]:
        """Serializa el resultado a diccionario."""
        return {
            "action_name": self.action_name,
            "status": self.status.value,
            "output": self.output,
            "error": self.error,
            "traceback": self.traceback,
            "duration_ms": self.duration_ms,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ActionResult":
        """Deserializa desde diccionario."""
        return cls(
            action_name=data["action_name"],
            status=ExecutionStatus(data["status"]),
            output=data.get("output"),
            error=data.get("error"),
            traceback=data.get("traceback"),
            duration_ms=data.get("duration_ms", 0.0),
            timestamp=data.get("timestamp", time.time()),
            metadata=data.get("metadata", {}),
        )


# ──────────────────────────────────────────────────────────────
# ExecutionSummary — resumen de un batch de ejecuciones
# ──────────────────────────────────────────────────────────────

@dataclass
class ExecutionSummary:
    """
    Resumen de la ejecución de un plan completo de acciones.
    
    Attributes:
        results: Lista de ActionResult individuales.
        total_actions: Total de acciones en el plan.
        successful: Cantidad de acciones exitosas.
        failed: Cantidad de acciones fallidas.
        skipped: Cantidad de acciones saltadas.
        total_duration_ms: Duración total del batch.
        all_success: True si todas las acciones fueron exitosas.
    """
    results: List[ActionResult] = field(default_factory=list)
    total_duration_ms: float = 0.0

    @property
    def total_actions(self) -> int:
        return len(self.results)

    @property
    def successful(self) -> int:
        return sum(1 for r in self.results if r.is_success)

    @property
    def failed(self) -> int:
        return sum(1 for r in self.results if r.is_failure)

    @property
    def skipped(self) -> int:
        return sum(1 for r in self.results if r.status == ExecutionStatus.SKIPPED)

    @property
    def all_success(self) -> bool:
        return self.total_actions > 0 and all(r.is_success for r in self.results)

    @property
    def has_failures(self) -> bool:
        return any(r.is_failure for r in self.results)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "results": [r.to_dict() for r in self.results],
            "total_actions": self.total_actions,
            "successful": self.successful,
            "failed": self.failed,
            "skipped": self.skipped,
            "total_duration_ms": self.total_duration_ms,
            "all_success": self.all_success,
        }


# ──────────────────────────────────────────────────────────────
# ActionExecutor
# ──────────────────────────────────────────────────────────────

class ActionExecutor:
    """
    Ejecutor de planes de acciones.
    
    Responsabilidades:
      1. Recibir un plan (lista de acciones con parámetros).
      2. Resolver cada acción en el ActionRegistry.
      3. Inyectar dependencias (ctx, memory) según metadata.
      4. Ejecutar secuencialmente con manejo de errores.
      5. Retornar ExecutionSummary con todos los resultados.
    
    Args:
        registry: ActionRegistry a utilizar (default: singleton).
        execution_tracker: Instancia opcional de ExecutionTracker (Sprint 028).
        default_timeout_ms: Timeout por defecto por acción (0 = sin timeout).
        fail_fast: Si True, detiene la ejecución ante el primer fallo.
    """

    def __init__(
        self,
        registry: Optional[ActionRegistry] = None,
        execution_tracker: Any = None,
        default_timeout_ms: float = 0.0,
        fail_fast: bool = False,
    ):
        self._registry = registry or get_default_registry()
        self._execution_tracker = execution_tracker
        self._default_timeout_ms = default_timeout_ms
        self._fail_fast = fail_fast

    @property
    def registry(self) -> ActionRegistry:
        return self._registry

    def execute_plan(
        self,
        plan: Dict[str, Any],
        ctx: Optional[Any] = None,
        memory: Optional[Any] = None,
    ) -> ExecutionSummary:
        """
        Ejecuta un plan de acciones completo.
        
        Args:
            plan: Diccionario con clave 'actions' (lista de dicts).
                  Cada dict tiene 'name' y opcionalmente 'params'.
            ctx: Contexto de sesión (inyectado si la acción lo requiere).
            memory: Instancia de memoria persistente (inyectado si requiere).
        
        Returns:
            ExecutionSummary con todos los resultados.
        """
        actions = plan.get("actions", [])
        if not isinstance(actions, list):
            return ExecutionSummary(
                results=[
                    ActionResult(
                        action_name="plan_validation",
                        status=ExecutionStatus.FAILED,
                        error="El plan debe contener una lista 'actions'.",
                    )
                ]
            )

        # Validar plan contra registro
        validation_errors = self._registry.validate_action_plan(plan)
        if validation_errors:
            return ExecutionSummary(
                results=[
                    ActionResult(
                        action_name="plan_validation",
                        status=ExecutionStatus.FAILED,
                        error="; ".join(validation_errors),
                    )
                ]
            )

        results: List[ActionResult] = []
        start_time = time.time()

        for idx, action_def in enumerate(actions):
            action_name = action_def.get("name", f"action_{idx}")
            params = action_def.get("params", {})
            
            result = self._execute_single(
                action_name=action_name,
                params=params,
                ctx=ctx,
                memory=memory,
                action_index=idx,
            )
            results.append(result)

            # Notificar al tracker si está disponible
            if self._execution_tracker is not None:
                self._notify_tracker(result)

            # Fail-fast
            if self._fail_fast and result.is_failure:
                break

        total_duration = (time.time() - start_time) * 1000
        return ExecutionSummary(results=results, total_duration_ms=total_duration)

    def execute_single(
        self,
        action_name: str,
        params: Optional[Dict[str, Any]] = None,
        ctx: Optional[Any] = None,
        memory: Optional[Any] = None,
    ) -> ActionResult:
        """
        Ejecuta una única acción por nombre.
        
        Args:
            action_name: Nombre de la acción registrada.
            params: Parámetros para la acción.
            ctx: Contexto de sesión.
            memory: Memoria persistente.
        
        Returns:
            ActionResult de la ejecución.
        """
        return self._execute_single(
            action_name=action_name,
            params=params or {},
            ctx=ctx,
            memory=memory,
            action_index=0,
        )

    def _execute_single(
        self,
        action_name: str,
        params: Dict[str, Any],
        ctx: Optional[Any],
        memory: Optional[Any],
        action_index: int,
    ) -> ActionResult:
        """Ejecución interna de una acción individual."""
        timestamp = time.time()
        
        try:
            action = self._registry.get(action_name)
        except ActionNotFoundError as e:
            return ActionResult(
                action_name=action_name,
                status=ExecutionStatus.FAILED,
                error=str(e),
                timestamp=timestamp,
            )

        # Preparar argumentos con inyección de dependencias
        call_args = dict(params)
        
        if action.metadata.requires_context and ctx is not None:
            call_args["ctx"] = ctx
        
        if action.metadata.requires_memory and memory is not None:
            call_args["memory"] = memory

        start = time.time()
        try:
            output = action.execute(**call_args)
            duration = (time.time() - start) * 1000
            
            return ActionResult(
                action_name=action_name,
                status=ExecutionStatus.SUCCESS,
                output=output,
                duration_ms=duration,
                timestamp=timestamp,
                metadata={
                    "action_index": action_index,
                    "action_version": action.metadata.version,
                },
            )
        except Exception as exc:
            duration = (time.time() - start) * 1000
            return ActionResult(
                action_name=action_name,
                status=ExecutionStatus.FAILED,
                error=str(exc),
                traceback=traceback.format_exc(),
                duration_ms=duration,
                timestamp=timestamp,
                metadata={
                    "action_index": action_index,
                    "action_version": action.metadata.version,
                },
            )

    def _notify_tracker(self, result: ActionResult) -> None:
        """Notifica al ExecutionTracker sobre un resultado."""
        if self._execution_tracker is None:
            return
        try:
            # Interfaz flexible: intenta métodos comunes
            if hasattr(self._execution_tracker, "record_execution"):
                self._execution_tracker.record_execution(result.to_dict())
            elif hasattr(self._execution_tracker, "track"):
                self._execution_tracker.track(result.to_dict())
            elif hasattr(self._execution_tracker, "log"):
                self._execution_tracker.log(result.to_dict())
        except Exception:
            # Silenciar errores del tracker para no romper ejecución
            pass

    def get_available_actions(self) -> List[str]:
        """Retorna lista de acciones disponibles en el registro."""
        return self._registry.action_names

    def describe_action(self, action_name: str) -> Optional[Dict[str, Any]]:
        """Describe una acción registrada."""
        try:
            action = self._registry.get(action_name)
            return {
                "name": action.metadata.name,
                "description": action.metadata.description,
                "version": action.metadata.version,
                "parameters": action.metadata.parameters,
                "returns": action.metadata.returns,
                "tags": action.metadata.tags,
                "requires_context": action.metadata.requires_context,
                "requires_memory": action.metadata.requires_memory,
            }
        except ActionNotFoundError:
            return None


# ──────────────────────────────────────────────────────────────
# Funciones de conveniencia
# ──────────────────────────────────────────────────────────────

def create_executor(
    registry: Optional[ActionRegistry] = None,
    execution_tracker: Any = None,
    fail_fast: bool = False,
) -> ActionExecutor:
    """Factory para crear un ActionExecutor configurado."""
    return ActionExecutor(
        registry=registry,
        execution_tracker=execution_tracker,
        fail_fast=fail_fast,
    )

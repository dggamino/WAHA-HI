"""
companion/pipeline_bridge.py

WAHA-HI Pipeline Integration Bridge — Sprint 032

Responsabilidad:
  - Conectar el Pipeline existente con el Action Execution Engine (031).
  - Actuar como fachada/adaptador sin modificar pipeline.py.
  - Recibir el plan del ActionPlanner (030) y orquestar su ejecucion.
  - Integrar resultados de acciones en el flujo del Pipeline.
  - Proveer hooks para que el Pipeline consuma resultados sin saber del Executor.

Diseno:
  - Bridge Pattern: el Pipeline interactua con una interfaz familiar.
  - El Bridge traduce llamadas del Pipeline al ActionExecutor.
  - Soporte para modo passthrough (sin acciones) para compatibilidad retroactiva.
  - Configurable: puede habilitarse/deshabilitarse sin tocar pipeline.py.

Compatibilidad:
  - 020-031 intactos.
  - No modifica pipeline.py, FlowOrchestrator, Responder, ni Planner.
  - Se inserta como capa traductora entre Planner y Execution Tracker.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Callable

from companion.action_registry import ActionRegistry, get_default_registry
from companion.action_executor import (
    ActionExecutor,
    ActionResult,
    ExecutionSummary,
    create_executor,
)


# ---------------------------------------------------------------
# PipelineBridgeResult — resultado expuesto al Pipeline
# ---------------------------------------------------------------

@dataclass
class PipelineBridgeResult:
    """
    Resultado de la integracion expuesto al Pipeline.
    
    Abstrae los detalles internos del ActionExecutor para que
    el Pipeline solo vea una interfaz familiar.
    
    Attributes:
        text: Texto principal para el Responder.
        metadata: Metadata acumulada de las acciones.
        action_results: Resultados crudos de cada accion ejecutada.
        execution_summary: Resumen completo de la ejecucion.
        has_actions: Si se ejecutaron acciones o fue passthrough.
        duration_ms: Duracion total del procesamiento.
    """
    text: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    action_results: List[ActionResult] = field(default_factory=list)
    execution_summary: Optional[ExecutionSummary] = None
    has_actions: bool = False
    duration_ms: float = 0.0

    @property
    def is_success(self) -> bool:
        """True si la ejecucion fue exitosa o no habia acciones."""
        if not self.has_actions:
            return True
        if self.execution_summary is not None:
            return self.execution_summary.all_success
        if self.action_results:
            return all(r.is_success for r in self.action_results)
        return True

    @property
    def has_failures(self) -> bool:
        """True si alguna accion fallo."""
        if not self.has_actions:
            return False
        if self.execution_summary is not None:
            return self.execution_summary.has_failures
        if self.action_results:
            return any(r.is_failure for r in self.action_results)
        return False

    def to_dict(self) -> Dict[str, Any]:
        """Serializa para consumo del Pipeline."""
        return {
            "text": self.text,
            "metadata": self.metadata,
            "has_actions": self.has_actions,
            "is_success": self.is_success,
            "has_failures": self.has_failures,
            "duration_ms": self.duration_ms,
            "action_results": [
                r.to_dict() for r in self.action_results
            ],
            "execution_summary": (
                self.execution_summary.to_dict()
                if self.execution_summary else None
            ),
        }


# ---------------------------------------------------------------
# PipelineBridge — capa de integracion
# ---------------------------------------------------------------

class PipelineBridge:
    """
    Puente de integracion entre Pipeline y Action Execution Engine.
    
    Responsabilidades:
      1. Recibir planes del ActionPlanner (030).
      2. Ejecutar planes via ActionExecutor (031).
      3. Transformar resultados en formato consumible por Pipeline.
      4. Inyectar resultados en el contexto de sesion.
      5. Proveer modo fallback si el Executor no esta disponible.
    
    Args:
        executor: ActionExecutor configurado (opcional).
        registry: ActionRegistry a utilizar (opcional).
        enabled: Si el bridge esta activo. Si False, actua como passthrough.
        text_extractor: Callable opcional para extraer texto de resultados.
    """

    def __init__(
        self,
        executor: Optional[ActionExecutor] = None,
        registry: Optional[ActionRegistry] = None,
        enabled: bool = True,
        text_extractor: Optional[Callable[[List[ActionResult]], str]] = None,
    ):
        self._executor = executor or create_executor(registry=registry)
        self._registry = registry or get_default_registry()
        self._enabled = enabled
        self._text_extractor = text_extractor or self._default_text_extractor

    @property
    def enabled(self) -> bool:
        """Estado del bridge."""
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self._enabled = value

    @property
    def executor(self) -> ActionExecutor:
        """El ActionExecutor subyacente."""
        return self._executor

    def process(
        self,
        plan: Optional[Dict[str, Any]] = None,
        ctx: Optional[Any] = None,
        memory: Optional[Any] = None,
        session_data: Optional[Dict[str, Any]] = None,
    ) -> PipelineBridgeResult:
        """
        Procesa un plan de acciones y retorna resultado integrado.
        
        Args:
            plan: Plan del ActionPlanner. None o sin acciones = passthrough.
            ctx: Contexto de sesion (para inyeccion en acciones).
            memory: Memoria persistente (para inyeccion en acciones).
            session_data: Datos adicionales de sesion para metadata.
        
        Returns:
            PipelineBridgeResult con todo listo para el Pipeline.
        """
        start_time = time.time()

        # Modo passthrough: no hay plan o el bridge esta deshabilitado
        if not self._enabled or plan is None or not plan.get("actions"):
            return PipelineBridgeResult(
                text="",
                metadata={"mode": "passthrough", "reason": "no_plan_or_disabled"},
                has_actions=False,
                duration_ms=(time.time() - start_time) * 1000,
            )

        # Ejecutar plan via ActionExecutor
        execution_summary = self._executor.execute_plan(
            plan=plan,
            ctx=ctx,
            memory=memory,
        )

        # Extraer texto acumulado de los resultados
        text = self._text_extractor(execution_summary.results)

        # Acumular metadata de todas las acciones exitosas
        metadata = self._extract_metadata(execution_summary.results)
        if session_data:
            metadata["session"] = session_data

        duration = (time.time() - start_time) * 1000

        return PipelineBridgeResult(
            text=text,
            metadata=metadata,
            action_results=execution_summary.results,
            execution_summary=execution_summary,
            has_actions=True,
            duration_ms=duration,
        )

    def process_single(
        self,
        action_name: str,
        params: Optional[Dict[str, Any]] = None,
        ctx: Optional[Any] = None,
        memory: Optional[Any] = None,
    ) -> PipelineBridgeResult:
        """
        Ejecuta una unica accion y retorna resultado integrado.
        
        Args:
            action_name: Nombre de la accion registrada.
            params: Parametros para la accion.
            ctx: Contexto de sesion.
            memory: Memoria persistente.
        
        Returns:
            PipelineBridgeResult.
        """
        start_time = time.time()

        if not self._enabled:
            return PipelineBridgeResult(
                text="",
                metadata={"mode": "passthrough", "reason": "disabled"},
                has_actions=False,
                duration_ms=(time.time() - start_time) * 1000,
            )

        result = self._executor.execute_single(
            action_name=action_name,
            params=params or {},
            ctx=ctx,
            memory=memory,
        )

        text = self._result_to_text(result)
        metadata = self._extract_metadata([result])

        duration = (time.time() - start_time) * 1000

        return PipelineBridgeResult(
            text=text,
            metadata=metadata,
            action_results=[result],
            has_actions=True,
            duration_ms=duration,
        )

    def inject_into_context(
        self,
        bridge_result: PipelineBridgeResult,
        ctx: Any,
        key: str = "action_results",
    ) -> None:
        """
        Inyecta el resultado del bridge en el contexto de sesion.
        
        Args:
            bridge_result: Resultado del bridge.
            ctx: Contexto de sesion (dict-like o con .set()).
            key: Clave bajo la cual almacenar.
        """
        payload = {
            "text": bridge_result.text,
            "metadata": bridge_result.metadata,
            "has_actions": bridge_result.has_actions,
            "is_success": bridge_result.is_success,
            "timestamp": time.time(),
        }
        if hasattr(ctx, "set"):
            ctx.set(key, payload)
        elif isinstance(ctx, dict):
            ctx[key] = payload

    def get_action_catalog(self) -> List[Dict[str, Any]]:
        """Retorna catalogo de acciones disponibles para el Planner."""
        from companion.actions.catalog import list_catalog_actions
        return list_catalog_actions()

    def describe_pipeline_flow(self) -> Dict[str, Any]:
        """Describe el flujo de integracion para documentacion."""
        return {
            "component": "PipelineBridge",
            "version": "0.1.0",
            "enabled": self._enabled,
            "flow": [
                "ActionPlanner (030) generates plan",
                "PipelineBridge receives plan",
                "ActionExecutor (031) executes actions",
                "PipelineBridge transforms results",
                "Results injected into session context",
                "ExecutionTracker (028) records execution",
                "FlowOrchestrator routes to Responder",
            ],
            "registry_size": len(self._registry),
            "available_actions": self._registry.action_names,
        }

    # ---------------------------------------------------------------
    # Metodos internos
    # ---------------------------------------------------------------

    @staticmethod
    def _default_text_extractor(results: List[ActionResult]) -> str:
        """Extrae texto concatenado de los resultados de acciones."""
        texts = []
        for result in results:
            if not result.is_success:
                continue
            output = result.output
            if isinstance(output, str):
                texts.append(output)
            elif isinstance(output, dict):
                if "text" in output:
                    texts.append(output["text"])
                elif "message" in output:
                    texts.append(output["message"])
        return "\n".join(texts)

    @staticmethod
    def _result_to_text(result: ActionResult) -> str:
        """Convierte un ActionResult individual a texto."""
        if not result.is_success:
            return ""
        output = result.output
        if isinstance(output, str):
            return output
        elif isinstance(output, dict) and "text" in output:
            return output["text"]
        return ""

    @staticmethod
    def _extract_metadata(results: List[ActionResult]) -> Dict[str, Any]:
        """Extrae y fusiona metadata de resultados exitosos."""
        metadata: Dict[str, Any] = {
            "actions_executed": len(results),
            "actions_successful": sum(1 for r in results if r.is_success),
            "actions_failed": sum(1 for r in results if r.is_failure),
        }
        for result in results:
            if result.is_success and isinstance(result.output, dict):
                if "metadata" in result.output:
                    metadata.update(result.output["metadata"])
        return metadata


# ---------------------------------------------------------------
# Factory y utilidades
# ---------------------------------------------------------------

def create_bridge(
    enabled: bool = True,
    fail_fast: bool = False,
    execution_tracker: Any = None,
) -> PipelineBridge:
    """
    Factory para crear un PipelineBridge configurado.
    
    Args:
        enabled: Si el bridge esta activo.
        fail_fast: Si el executor debe detenerse ante el primer fallo.
        execution_tracker: Instancia de tracker para el executor.
    
    Returns:
        PipelineBridge configurado.
    """
    executor = create_executor(
        fail_fast=fail_fast,
        execution_tracker=execution_tracker,
    )
    return PipelineBridge(executor=executor, enabled=enabled)

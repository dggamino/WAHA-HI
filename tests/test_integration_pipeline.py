"""
tests/test_integration_pipeline.py

WAHA-HI End-to-End Integration Test Suite — Sprint 033

Responsabilidad:
  - Validar la integracion completa de la cadena 030-032.
  - Simular flujos reales del Pipeline sin modificarlo.
  - Probar la interaccion entre: Planner -> Bridge -> Executor -> Tracker.
  - Verificar compatibilidad retroactiva (passthrough mode).
  - Asegurar que los resultados son consumibles por FlowOrchestrator/Responder.

Diseno:
  - Tests de integracion que usan los componentes como caja negra.
  - Fixtures para setup/teardown limpio.
  - Escenarios: flujo completo, passthrough, fallo, fallback.
  - No depende de pipeline.py (que no se modifica).

Compatibilidad:
  - 020-032 intactos.
  - No modifica ningun archivo de produccion.
  - Solo agrega tests.
"""

from __future__ import annotations

import unittest
import importlib
from typing import Any, Dict, List, Optional

# Importar componentes del sistema
from companion.action_registry import (
    register_action,
    reset_registry,
    get_default_registry,
    ActionRegistry,
)
from companion.action_executor import (
    ActionExecutor,
    create_executor,
    ExecutionStatus,
    ActionResult,
    ExecutionSummary,
)
from companion.pipeline_bridge import (
    PipelineBridge,
    PipelineBridgeResult,
    create_bridge,
)
from companion.actions.context import ActionContext
from companion.actions.memory import ActionMemory
from companion.actions.response import ActionResponseBuilder


# ===============================================================
# FIXTURES Y UTILIDADES
# ===============================================================

class MockExecutionTracker:
    """Mock del ExecutionTracker (Sprint 028) para tests."""
    
    def __init__(self):
        self.records: List[Dict[str, Any]] = []
    
    def record_execution(self, data: Dict[str, Any]) -> None:
        self.records.append(data)
    
    def clear(self) -> None:
        self.records.clear()


class MockSessionContext:
    """Mock de contexto de sesion para tests."""
    
    def __init__(self, data: Optional[Dict[str, Any]] = None):
        self._data = data or {}
    
    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        self._data[key] = value
    
    def to_dict(self) -> Dict[str, Any]:
        return dict(self._data)


def setup_test_registry() -> ActionRegistry:
    """Limpia y configura el registro para tests."""
    reset_registry()
    
    # Importar y recargar catalog para registrar acciones built-in
    import companion.actions.catalog
    importlib.reload(companion.actions.catalog)
    
    reg = get_default_registry()
    
    # Acciones de prueba adicionales
    @register_action(name="test/greet", description="Saluda al usuario")
    def test_greet(name: str) -> str:
        return f"Hola, {name}!"
    
    @register_action(name="test/calc", description="Operacion matematica")
    def test_calc(a: float, b: float, op: str = "add") -> Dict[str, Any]:
        if op == "add":
            result = a + b
        elif op == "mul":
            result = a * b
        else:
            raise ValueError(f"Operacion desconocida: {op}")
        return {"result": result, "operation": op, "operands": [a, b]}
    
    @register_action(name="test/build_response", description="Construye respuesta")
    def test_build_response(text: str, confidence: float = 1.0) -> Dict[str, Any]:
        return {
            "text": text,
            "metadata": {"confidence": confidence, "source": "test"},
        }
    
    @register_action(name="test/use_context", description="Usa contexto", requires_context=True)
    def test_use_context(ctx: Any) -> str:
        return f"Session: {ctx.get('session_id', 'unknown')}"
    
    @register_action(name="test/use_memory", description="Usa memoria", requires_memory=True)
    def test_use_memory(memory: Any) -> str:
        return f"Stored: {memory.recall('test_key', 'not_found')}"
    
    @register_action(name="test/fail", description="Siempre falla")
    def test_fail():
        raise RuntimeError("Error forzado para testing")
    
    return reg


# ===============================================================
# TESTS DE INTEGRACION
# ===============================================================

class TestActionRegistryIntegration(unittest.TestCase):
    """Tests de integracion para ActionRegistry (031)."""
    
    def setUp(self):
        self.registry = setup_test_registry()
    
    def tearDown(self):
        reset_registry()
    
    def test_registry_has_all_test_actions(self):
        """El registro contiene todas las acciones de prueba."""
        actions = self.registry.action_names
        self.assertIn("test/greet", actions)
        self.assertIn("test/calc", actions)
        self.assertIn("test/build_response", actions)
        self.assertIn("test/use_context", actions)
        self.assertIn("test/use_memory", actions)
        self.assertIn("test/fail", actions)
    
    def test_registry_has_builtin_actions(self):
        """El registro contiene acciones built-in del catalogo."""
        actions = self.registry.action_names
        self.assertIn("core/echo", actions)
        self.assertIn("core/noop", actions)
        self.assertIn("memory/store", actions)
        self.assertIn("context/get", actions)
        self.assertIn("response/build", actions)
    
    def test_registry_metadata_extraction(self):
        """Los metadatos se extraen correctamente de las firmas."""
        action = self.registry.get("test/calc")
        params = action.metadata.parameters
        param_names = [p["name"] for p in params]
        self.assertIn("a", param_names)
        self.assertIn("b", param_names)
        self.assertIn("op", param_names)
        # op tiene default, no es required
        op_param = next(p for p in params if p["name"] == "op")
        self.assertFalse(op_param["required"])
    
    def test_registry_dependency_flags(self):
        """Las flags de dependencia se detectan correctamente."""
        ctx_action = self.registry.get("test/use_context")
        self.assertTrue(ctx_action.metadata.requires_context)
        self.assertFalse(ctx_action.metadata.requires_memory)
        
        mem_action = self.registry.get("test/use_memory")
        self.assertFalse(mem_action.metadata.requires_context)
        self.assertTrue(mem_action.metadata.requires_memory)
    
    def test_registry_plan_validation_valid(self):
        """Un plan valido pasa la validacion."""
        plan = {
            "actions": [
                {"name": "test/greet", "params": {"name": "Usuario"}},
                {"name": "test/calc", "params": {"a": 5, "b": 3}},
            ]
        }
        errors = self.registry.validate_action_plan(plan)
        self.assertEqual(errors, [])
    
    def test_registry_plan_validation_missing_action(self):
        """Un plan con accion inexistente falla validacion."""
        plan = {
            "actions": [
                {"name": "test/greet", "params": {"name": "Usuario"}},
                {"name": "test/no_existe", "params": {}},
            ]
        }
        errors = self.registry.validate_action_plan(plan)
        self.assertEqual(len(errors), 1)
        self.assertIn("no_existe", errors[0])
    
    def test_registry_plan_validation_missing_params(self):
        """Un plan con parametros faltantes falla validacion."""
        plan = {
            "actions": [
                {"name": "test/greet", "params": {}},  # falta 'name'
            ]
        }
        errors = self.registry.validate_action_plan(plan)
        self.assertEqual(len(errors), 1)
        self.assertIn("name", errors[0])


class TestActionExecutorIntegration(unittest.TestCase):
    """Tests de integracion para ActionExecutor (031)."""
    
    def setUp(self):
        self.registry = setup_test_registry()
        self.tracker = MockExecutionTracker()
        self.executor = create_executor(execution_tracker=self.tracker)
    
    def tearDown(self):
        reset_registry()
    
    def test_execute_plan_success(self):
        """Un plan valido se ejecuta exitosamente."""
        plan = {
            "actions": [
                {"name": "test/greet", "params": {"name": "WAHA-HI"}},
                {"name": "test/calc", "params": {"a": 10, "b": 20, "op": "add"}},
            ]
        }
        summary = self.executor.execute_plan(plan)
        
        self.assertTrue(summary.all_success)
        self.assertEqual(summary.total_actions, 2)
        self.assertEqual(summary.successful, 2)
        self.assertEqual(summary.failed, 0)
        self.assertEqual(summary.results[0].output, "Hola, WAHA-HI!")
        self.assertEqual(summary.results[1].output["result"], 30)
    
    def test_execute_plan_with_tracker(self):
        """El tracker recibe registros de cada ejecucion."""
        plan = {
            "actions": [
                {"name": "test/greet", "params": {"name": "Test"}},
            ]
        }
        self.executor.execute_plan(plan)
        
        self.assertEqual(len(self.tracker.records), 1)
        self.assertEqual(self.tracker.records[0]["action_name"], "test/greet")
        self.assertEqual(self.tracker.records[0]["status"], "success")
    
    def test_execute_plan_with_failure(self):
        """Un plan con fallo maneja el error correctamente."""
        plan = {
            "actions": [
                {"name": "test/greet", "params": {"name": "A"}},
                {"name": "test/fail", "params": {}},
                {"name": "test/greet", "params": {"name": "B"}},
            ]
        }
        summary = self.executor.execute_plan(plan)
        
        self.assertFalse(summary.all_success)
        self.assertEqual(summary.successful, 2)
        self.assertEqual(summary.failed, 1)
        self.assertIsNotNone(summary.results[1].traceback)
    
    def test_execute_plan_fail_fast(self):
        """Fail-fast detiene la ejecucion ante el primer fallo."""
        executor_ff = create_executor(
            execution_tracker=self.tracker,
            fail_fast=True,
        )
        plan = {
            "actions": [
                {"name": "test/greet", "params": {"name": "A"}},
                {"name": "test/fail", "params": {}},
                {"name": "test/greet", "params": {"name": "B"}},
            ]
        }
        summary = executor_ff.execute_plan(plan)
        
        self.assertEqual(summary.total_actions, 2)  # Se detuvo
        self.assertEqual(summary.successful, 1)
    
    def test_execute_plan_with_context(self):
        """La inyeccion de contexto funciona."""
        plan = {
            "actions": [
                {"name": "test/use_context", "params": {}},
            ]
        }
        ctx = MockSessionContext({"session_id": "sess_123"})
        summary = self.executor.execute_plan(plan, ctx=ctx)
        
        self.assertTrue(summary.all_success)
        self.assertIn("sess_123", summary.results[0].output)
    
    def test_execute_plan_with_memory(self):
        """La inyeccion de memoria funciona."""
        plan = {
            "actions": [
                {"name": "test/use_memory", "params": {}},
            ]
        }
        mem = ActionMemory({"test_key": "valor_test"})
        summary = self.executor.execute_plan(plan, memory=mem)
        
        self.assertTrue(summary.all_success)
        self.assertIn("valor_test", summary.results[0].output)
    
    def test_execute_single_action(self):
        """Ejecutar una accion individual funciona."""
        result = self.executor.execute_single(
            action_name="test/greet",
            params={"name": "Single"},
        )
        
        self.assertTrue(result.is_success)
        self.assertEqual(result.output, "Hola, Single!")
    
    def test_execute_invalid_plan(self):
        """Un plan malformado retorna error estructurado."""
        plan = {"actions": "no_es_lista"}
        summary = self.executor.execute_plan(plan)
        
        self.assertFalse(summary.all_success)
        self.assertEqual(summary.total_actions, 1)
        self.assertIn("lista", summary.results[0].error.lower())


class TestPipelineBridgeIntegration(unittest.TestCase):
    """Tests de integracion para PipelineBridge (032)."""
    
    def setUp(self):
        self.registry = setup_test_registry()
        self.tracker = MockExecutionTracker()
        self.bridge = create_bridge(execution_tracker=self.tracker)
    
    def tearDown(self):
        reset_registry()
    
    def test_bridge_process_full_flow(self):
        """Flujo completo: plan -> bridge -> resultados estructurados."""
        plan = {
            "actions": [
                {"name": "test/greet", "params": {"name": "Usuario"}},
                {"name": "test/build_response", "params": {"text": "Respuesta"}},
            ]
        }
        result = self.bridge.process(plan=plan)
        
        self.assertTrue(result.is_success)
        self.assertTrue(result.has_actions)
        self.assertIn("Hola, Usuario!", result.text)
        self.assertIn("Respuesta", result.text)
        self.assertEqual(result.metadata["actions_executed"], 2)
        self.assertEqual(result.metadata["actions_successful"], 2)
    
    def test_bridge_passthrough_no_plan(self):
        """Sin plan, el bridge actua en modo passthrough."""
        result = self.bridge.process(plan=None)
        
        self.assertFalse(result.has_actions)
        self.assertTrue(result.is_success)
        self.assertEqual(result.metadata.get("mode"), "passthrough")
    
    def test_bridge_passthrough_disabled(self):
        """Con bridge deshabilitado, actua en modo passthrough."""
        self.bridge.enabled = False
        plan = {
            "actions": [
                {"name": "test/greet", "params": {"name": "Test"}},
            ]
        }
        result = self.bridge.process(plan=plan)
        
        self.assertFalse(result.has_actions)
        self.assertEqual(result.metadata.get("mode"), "passthrough")
    
    def test_bridge_process_single(self):
        """Ejecutar accion individual via bridge."""
        result = self.bridge.process_single(
            action_name="test/greet",
            params={"name": "Mundo"},
        )
        
        self.assertTrue(result.is_success)
        self.assertTrue(result.has_actions)
        self.assertEqual(result.text, "Hola, Mundo!")
    
    def test_bridge_inject_into_context(self):
        """Los resultados se inyectan correctamente en el contexto."""
        plan = {
            "actions": [
                {"name": "test/greet", "params": {"name": "CtxTest"}},
            ]
        }
        result = self.bridge.process(plan=plan)
        ctx = MockSessionContext()
        
        self.bridge.inject_into_context(result, ctx)
        
        injected = ctx.get("action_results")
        self.assertIsNotNone(injected)
        self.assertTrue(injected["is_success"])
        self.assertIn("CtxTest", injected["text"])
    
    def test_bridge_with_session_data(self):
        """Los session_data se incorporan a la metadata."""
        plan = {
            "actions": [
                {"name": "test/greet", "params": {"name": "User"}},
            ]
        }
        result = self.bridge.process(
            plan=plan,
            session_data={"user_id": "u123", "turn": 3},
        )
        
        self.assertIn("session", result.metadata)
        self.assertEqual(result.metadata["session"]["user_id"], "u123")
    
    def test_bridge_with_dependencies(self):
        """El bridge maneja inyeccion de ctx y memory."""
        plan = {
            "actions": [
                {"name": "test/use_context", "params": {}},
                {"name": "test/use_memory", "params": {}},
            ]
        }
        ctx = MockSessionContext({"session_id": "abc"})
        mem = ActionMemory({"test_key": "val"})
        
        result = self.bridge.process(plan=plan, ctx=ctx, memory=mem)
        
        self.assertTrue(result.is_success)
        self.assertIn("abc", result.text)
        self.assertIn("val", result.text)
    
    def test_bridge_catalog_builtin(self):
        """El bridge expone el catalogo de acciones built-in."""
        catalog = self.bridge.get_action_catalog()
        names = [a["name"] for a in catalog]
        
        # El catalogo built-in incluye core/, memory/, context/, response/
        self.assertTrue(len(names) > 0)
        has_builtin = any(n.startswith(("core/", "memory/", "context/", "response/")) for n in names)
        self.assertTrue(has_builtin)
    
    def test_bridge_catalog_all_actions(self):
        """El registro contiene todas las acciones (test + built-in)."""
        all_actions = self.bridge.executor.registry.action_names
        self.assertIn("test/greet", all_actions)
        self.assertIn("core/echo", all_actions)
    
    def test_bridge_describe_flow(self):
        """El bridge describe su flujo de integracion."""
        flow = self.bridge.describe_pipeline_flow()
        
        self.assertEqual(flow["component"], "PipelineBridge")
        self.assertEqual(flow["version"], "0.1.0")
        self.assertTrue(flow["enabled"])
        self.assertEqual(len(flow["flow"]), 7)
    
    def test_bridge_result_serialization(self):
        """El resultado del bridge es serializable."""
        plan = {
            "actions": [
                {"name": "test/greet", "params": {"name": "Serial"}},
            ]
        }
        result = self.bridge.process(plan=plan)
        data = result.to_dict()
        
        self.assertIn("text", data)
        self.assertIn("metadata", data)
        self.assertIn("action_results", data)
        self.assertIn("execution_summary", data)
        self.assertTrue(data["is_success"])


class TestEndToEndFlow(unittest.TestCase):
    """Tests end-to-end de la cadena completa."""
    
    def setUp(self):
        self.registry = setup_test_registry()
        self.tracker = MockExecutionTracker()
        self.bridge = create_bridge(execution_tracker=self.tracker)
    
    def tearDown(self):
        reset_registry()
    
    def test_e2e_simple_conversation_turn(self):
        """
        Simula un turno de conversacion completo:
        Planner genera plan -> Bridge ejecuta -> Resultados listos para Responder
        """
        # 1. Planner genera plan (simulado)
        plan = {
            "actions": [
                {"name": "test/greet", "params": {"name": "Usuario"}},
                {"name": "test/build_response", "params": {
                    "text": "Bienvenido al sistema WAHA-HI",
                    "confidence": 0.95,
                }},
            ]
        }
        
        # 2. Bridge procesa el plan
        ctx = MockSessionContext({"session_id": "sess_001", "user_id": "user_42"})
        result = self.bridge.process(plan=plan, ctx=ctx)
        
        # 3. Verificar resultados para Responder
        self.assertTrue(result.is_success)
        self.assertTrue(result.has_actions)
        self.assertIn("Hola, Usuario!", result.text)
        self.assertIn("Bienvenido", result.text)
        self.assertEqual(result.metadata["actions_executed"], 2)
        self.assertEqual(result.metadata["confidence"], 0.95)
        
        # 4. Verificar que el tracker recibio los registros
        self.assertEqual(len(self.tracker.records), 2)
        
        # 5. Inyectar en contexto para siguiente turno
        self.bridge.inject_into_context(result, ctx)
        self.assertIn("action_results", ctx.to_dict())
    
    def test_e2e_with_memory_persistence(self):
        """
        Simula flujo con memoria persistente entre turnos.
        """
        mem = ActionMemory({})
        
        # Turno 1: Almacenar preferencia
        plan1 = {
            "actions": [
                {"name": "test/use_memory", "params": {}},
            ]
        }
        # Primero guardamos algo en memoria
        mem.store("test_key", "preferencia_usuario")
        
        result1 = self.bridge.process(plan=plan1, memory=mem)
        self.assertIn("preferencia_usuario", result1.text)
        
        # Turno 2: Recuperar preferencia
        result2 = self.bridge.process(plan=plan1, memory=mem)
        self.assertIn("preferencia_usuario", result2.text)
    
    def test_e2e_failure_recovery(self):
        """
        Simula flujo donde una accion falla pero el sistema continua.
        (sin fail-fast, todas las acciones se intentan)
        """
        plan = {
            "actions": [
                {"name": "test/greet", "params": {"name": "A"}},
                {"name": "test/fail", "params": {}},
                {"name": "test/greet", "params": {"name": "B"}},
            ]
        }
        
        result = self.bridge.process(plan=plan)
        
        # El bridge reporta el fallo pero no colapsa
        self.assertTrue(result.has_actions)
        self.assertTrue(result.has_failures)
        self.assertIn("A", result.text)  # La primera accion si funciono
        self.assertIn("B", result.text)  # La tercera tambien (sin fail-fast)
        self.assertEqual(result.metadata["actions_executed"], 3)
        self.assertEqual(result.metadata["actions_successful"], 2)
        self.assertEqual(result.metadata["actions_failed"], 1)
    
    def test_e2e_failure_recovery_fail_fast(self):
        """
        Simula flujo con fail-fast: se detiene ante el primer fallo.
        """
        bridge_ff = create_bridge(execution_tracker=self.tracker, fail_fast=True)
        plan = {
            "actions": [
                {"name": "test/greet", "params": {"name": "A"}},
                {"name": "test/fail", "params": {}},
                {"name": "test/greet", "params": {"name": "B"}},
            ]
        }
        
        result = bridge_ff.process(plan=plan)
        
        self.assertTrue(result.has_failures)
        self.assertIn("A", result.text)
        self.assertNotIn("B", result.text)  # No se ejecuto por fail-fast
    
    def test_e2e_passthrough_backward_compatibility(self):
        """
        Verifica que el sistema funciona en modo passthrough
        cuando no hay plan (compatibilidad con 020-029).
        """
        result = self.bridge.process(plan=None)
        
        self.assertFalse(result.has_actions)
        self.assertTrue(result.is_success)
        self.assertEqual(result.text, "")
        
        # El Pipeline puede continuar sin acciones ejecutadas
        # FlowOrchestrator maneja el caso de no-action normalmente
    
    def test_e2e_response_builder_integration(self):
        """
        Verifica que ActionResponseBuilder funciona con resultados del bridge.
        """
        plan = {
            "actions": [
                {"name": "test/greet", "params": {"name": "Builder"}},
                {"name": "test/build_response", "params": {"text": "Linea 2"}},
            ]
        }
        
        result = self.bridge.process(plan=plan)
        
        # Construir respuesta con el builder
        builder = ActionResponseBuilder.from_action_results(result.action_results)
        builder.add_metadata(bridge_version="0.1.0")
        response = builder.build()
        
        self.assertIn("Builder", response["text"])
        self.assertIn("Linea 2", response["text"])
        self.assertEqual(response["metadata"]["bridge_version"], "0.1.0")
        self.assertEqual(response["type"], "companion_response")


# ===============================================================
# EJECUCION
# ===============================================================

if __name__ == "__main__":
    unittest.main(verbosity=2)

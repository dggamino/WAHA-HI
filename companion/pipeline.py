"""
Companion Pipeline Foundation v1.1.0

IMPLEMENTAR 030
Adaptive Action Planning Foundation
"""


from .intents.classifier import classify

from .flows import FlowOrchestrator

from .responders import get_responder

from .session import Session


from .context import (
    ContextLifecycleManager,
    ConversationResolver,
)


from .memory import MemoryManager

from .memory_intelligence import MemoryIntelligence

from .semantic_memory import SemanticMemoryRetriever

from .flow_selector import MemoryFlowSelector

from .decision_layer import DecisionLayer

from .action_planner import ActionPlanner

from .execution_tracker import ExecutionTracker

from .goal_detector import GoalDetector




class CompanionPipeline:


    def __init__(self):

        self.orchestrator = FlowOrchestrator()

        self.responder = get_responder()

        self.context_manager = ContextLifecycleManager()

        self.resolver = ConversationResolver()

        self.memory_manager = MemoryManager()

        self.semantic_memory = SemanticMemoryRetriever(
            self.memory_manager
        )

        self.memory_intelligence = MemoryIntelligence()

        self.flow_selector = MemoryFlowSelector()

        self.decision_layer = DecisionLayer()

        self.goal_detector = GoalDetector()

        self.action_planner = ActionPlanner()

        self.execution_tracker = ExecutionTracker()



    def handle(
        self,
        message,
        context=None,
        session=None,
        session_id=None
    ):


        if session is None:

            session = Session(
                session_id=session_id,
                channel="internal"
            )


        semantic_memory = self.semantic_memory.retrieve(
            session.id,
            message
        )


        selected_flow = self.flow_selector.select(
            message,
            semantic_memory
        )


        decision = self.decision_layer.decide(
            message,
            semantic_memory,
            selected_flow
        )


        if context is None:

            context = self.context_manager.create_context(
                session
            )


        context_data = context.to_dict()


        context_data["memory"] = semantic_memory


        resolved_message = self.resolver.resolve(
            message,
            context_data
        )


        if decision.get(
            "action"
        ) in [
            "continue_flow",
            "resume_context"
        ]:

            intent = decision["intent"]

        else:

            intent = classify(
                resolved_message
            )


        goal = self.goal_detector.detect(
            intent,
            context_data,
            message
        )


        plan = self.action_planner.plan(
            intent,
            goal,
            decision,
            message
        )


        execution = self.execution_tracker.create(
            plan,
            session.id
        )


        self.execution_tracker.start(
            execution
        )


        self.context_manager.update_context(
            context,
            intent=intent,
            state="INTENT_DETECTED"
        )


        result = self.orchestrator.route(
            intent,
            context
        )


        self.context_manager.update_context(
            context,
            state="FLOW_ACTIVE"
        )


        response = self.responder.build(
            result
        )


        self.execution_tracker.complete(
            execution,
            result
        )


        intelligent_memory = self.memory_intelligence.enrich(
            message,
            intent,
            result
        )


        context.memory = intelligent_memory


        self.context_manager.persist_context(
            context
        )


        self.memory_manager.remember(
            session.id,
            intelligent_memory
        )


        return {
            "intent": intent,
            "goal": goal,
            "decision": decision,
            "plan": plan,
            "execution": execution,
            "message": resolved_message,
            "result": result,
            "response": response,
            "memory": intelligent_memory,
            "semantic_memory": semantic_memory,
            "session_id": session.id
        }

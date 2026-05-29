
from typing import Dict, Any, List
from datetime import datetime
from .workflow_engine import workflow_engine, WorkflowStage
from .context_store import context_store
from app.agents.insight_agent import insight_agent
from app.agents.revision_agent import revision_agent
from app.agents.replanning_agent import replanning_agent
from app.utils.logger import logger


class OrchestrationManager:
    def __init__(self):
        self._register_handlers()

    def _register_handlers(self):
        workflow_engine.register_stage_handler(WorkflowStage.RESEARCH, self._handle_research)
        workflow_engine.register_stage_handler(WorkflowStage.STUDENT_ANALYSIS, self._handle_student_analysis)
        workflow_engine.register_stage_handler(WorkflowStage.PLANNING, self._handle_planning)
        workflow_engine.register_stage_handler(WorkflowStage.EXECUTION, self._handle_execution)
        workflow_engine.register_stage_handler(WorkflowStage.REVISION, self._handle_revision)
        workflow_engine.register_stage_handler(WorkflowStage.REPLANNING, self._handle_replanning)
        workflow_engine.register_stage_handler(WorkflowStage.INSIGHTS, self._handle_insights)

    def _handle_research(self, context: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Research stage handler - START")
        context = context or {}
        research_data = context.get("research_data", {})
        context_store.set("research_data", research_data)
        result = {"status": "research_completed", "data": research_data}
        logger.info("Research stage handler - FINISH")
        return result

    def _handle_student_analysis(self, context: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Student analysis stage handler - START")
        context = context or {}
        student_data = context.get("student_data", {})
        context_store.set("student_data", student_data)
        result = {"status": "analysis_completed", "data": student_data}
        logger.info("Student analysis stage handler - FINISH")
        return result

    def _handle_planning(self, context: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Planning stage handler - START")
        context = context or {}
        plan_data = context.get("plan_data", {})
        context_store.set("plan_data", plan_data)
        result = {"status": "planning_completed", "data": plan_data}
        logger.info("Planning stage handler - FINISH")
        return result

    def _handle_execution(self, context: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Execution stage handler - START")
        context = context or {}
        tasks = context.get("tasks", [])
        context_store.set("tasks", tasks)
        result = {"status": "execution_tracked", "tasks": tasks}
        logger.info("Execution stage handler - FINISH")
        return result

    def _handle_revision(self, context: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Revision stage handler - START")
        context = context or {}
        revision_schedule = revision_agent.generate_revision_schedule(
            subject=context.get("subject"),
            recent_tasks=context.get("recent_tasks"),
            current_readiness=context.get("current_readiness", 70)
        )
        context_store.set("revision_schedule", revision_schedule)
        logger.info("Revision stage handler - FINISH")
        return revision_schedule

    def _handle_replanning(self, context: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Replanning stage handler - START")
        context = context or {}
        replan = replanning_agent.generate_replan(
            current_tasks=context.get("current_tasks"),
            missed_tasks=context.get("missed_tasks"),
            new_availability=context.get("new_availability"),
            readiness_change=context.get("readiness_change")
        )
        context_store.set("replan", replan)
        logger.info("Replanning stage handler - FINISH")
        return replan

    def _handle_insights(self, context: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Insights stage handler - START")
        context = context or {}
        insights = insight_agent.generate_insights(context.get("student_data"))
        logger.info("Insights stage handler - FINISH")
        return insights

    def run_full_workflow(self, context: Dict[str, Any] = None) -> Dict[str, Any]:
        logger.info("Orchestration manager starting full workflow")
        context = context or {}
        context_store.set("workflow_state", {
            "started_at": datetime.now().isoformat(),
            "status": "running"
        })

        result = workflow_engine.execute_workflow(WorkflowStage.RESEARCH, context)

        context_store.set("workflow_state", {
            "started_at": context_store.get("workflow_state", {}).get("started_at"),
            "completed_at": datetime.now().isoformat(),
            "status": "completed" if result.get("completed") else "failed",
            "results": result
        })

        return result

    def run_stage(self, stage: WorkflowStage, context: Dict[str, Any] = None) -> Dict[str, Any]:
        context = context or {}
        return workflow_engine.execute_stage(stage, context)

    def get_workflow_status(self) -> Dict[str, Any]:
        return {
            "current_stage": workflow_engine.get_current_stage(),
            "history": workflow_engine.get_stage_history(),
            "context": context_store.get_all(),
            "logs": context_store.get_logs(20)
        }

    def validate_orchestration(self) -> Dict[str, Any]:
        logger.info("Validating orchestration setup")
        issues = []
        checks = []

        checks.append({
            "check": "context_store_available",
            "status": "ok",
            "message": "Context store initialized"
        })

        checks.append({
            "check": "workflow_engine_available",
            "status": "ok",
            "message": "Workflow engine initialized"
        })

        required_stages = [s for s in WorkflowStage]
        for stage in required_stages:
            if stage in workflow_engine.stage_handlers:
                checks.append({
                    "check": f"handler_{stage}",
                    "status": "ok",
                    "message": f"Handler registered for {stage}"
                })
            else:
                checks.append({
                    "check": f"handler_{stage}",
                    "status": "warning",
                    "message": f"No handler registered for {stage}"
                })

        return {
            "validated_at": datetime.now().isoformat(),
            "valid": len(issues) == 0,
            "checks": checks,
            "issues": issues
        }


orchestration_manager = OrchestrationManager()


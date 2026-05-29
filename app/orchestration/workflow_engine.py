
from typing import Dict, Any, List, Callable, Optional
from datetime import datetime
from enum import Enum
from app.utils.logger import logger


class WorkflowStage(str, Enum):
    RESEARCH = "research"
    STUDENT_ANALYSIS = "student_analysis"
    PLANNING = "planning"
    EXECUTION = "execution"
    REVISION = "revision"
    REPLANNING = "replanning"
    INSIGHTS = "insights"


class WorkflowEngine:
    def __init__(self):
        self.stages = list(WorkflowStage)
        self.current_stage: Optional[WorkflowStage] = None
        self.stage_history: List[Dict[str, Any]] = []
        self.stage_handlers: Dict[WorkflowStage, Callable] = {}

    def register_stage_handler(self, stage: WorkflowStage, handler: Callable):
        self.stage_handlers[stage] = handler

    def execute_stage(self, stage: WorkflowStage, context: Dict[str, Any] = None) -> Dict[str, Any]:
        self.current_stage = stage
        logger.info(f"===== EXECUTING WORKFLOW STAGE: {stage} =====")

        start_time = datetime.now()
        result = {"stage": stage.value, "start_time": start_time.isoformat()}

        try:
            safe_context = context or {}
            if stage in self.stage_handlers:
                handler_result = self.stage_handlers[stage](safe_context)
                result.update({
                    "success": True,
                    "data": handler_result,
                    "end_time": datetime.now().isoformat()
                })
                logger.info(f"===== STAGE {stage} COMPLETED SUCCESSFULLY =====")
            else:
                result.update({
                    "success": True,
                    "message": f"No handler registered for {stage}, stage completed"
                })
                logger.info(f"===== STAGE {stage} COMPLETED (NO HANDLER) =====")
        except Exception as e:
            logger.error(f"===== STAGE {stage} FAILED: {e} =====")
            result.update({
                "success": False,
                "error": str(e)
            })

        self.stage_history.append(result)
        return result

    def execute_workflow(self, start_stage: WorkflowStage = WorkflowStage.RESEARCH, context: Dict[str, Any] = None) -> Dict[str, Any]:
        logger.info("===== STARTING FULL WORKFLOW EXECUTION =====")
        workflow_results = []
        current_idx = self.stages.index(start_stage)

        for i in range(current_idx, len(self.stages)):
            stage = self.stages[i]
            result = self.execute_stage(stage, context)
            workflow_results.append(result)
            if not result.get("success"):
                logger.warning(f"===== WORKFLOW STOPPED AT STAGE {stage} =====")
                break

        completed = all(r.get("success") for r in workflow_results)
        logger.info(f"===== WORKFLOW EXECUTION FINISHED: COMPLETED = {completed} =====")

        return {
            "workflow_id": datetime.now().isoformat(),
            "results": workflow_results,
            "completed": completed
        }

    def get_current_stage(self) -> Optional[WorkflowStage]:
        return self.current_stage

    def get_stage_history(self) -> List[Dict[str, Any]]:
        return self.stage_history.copy()

    def reset_workflow(self):
        self.current_stage = None
        self.stage_history = []
        logger.info("Workflow reset")


workflow_engine = WorkflowEngine()


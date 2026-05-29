
from fastapi import APIRouter, HTTPException
from app.schemas.tasks import (
    Task, TaskCreate, TaskUpdate, TaskListResponse, TaskResponse,
    RevisionRequest, RevisionResponse, ReplanningRequest, ReplanningResponse,
    InsightRequest, InsightResponse, WorkflowStatusResponse, WorkflowRunRequest
)
from app.schemas.common import StudentAnalysisRequest, StudentAnalysisResponse, AgentsStatusResponse, AgentStatus
from app.database.task_store import task_store
from app.agents.revision_agent import revision_agent
from app.agents.replanning_agent import replanning_agent
from app.agents.insight_agent import insight_agent
from app.orchestration.orchestration_manager import orchestration_manager
from app.utils.logger import logger


router = APIRouter(tags=["Tasks"], prefix="/tasks")


@router.get("", response_model=TaskListResponse)
async def get_tasks():
    logger.info("Fetching all tasks")
    tasks = task_store.get_all_tasks()
    return TaskListResponse(success=True, data=tasks, count=len(tasks))


@router.post("", response_model=TaskResponse)
async def create_task(task: TaskCreate):
    logger.info(f"Creating new task: {task.title}")
    created_task = task_store.create_task(task)
    return TaskResponse(success=True, data=created_task)


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: str, task_update: TaskUpdate):
    logger.info(f"Updating task {task_id}")
    updated_task = task_store.update_task(task_id, task_update)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponse(success=True, data=updated_task)


@router.delete("/{task_id}")
async def delete_task(task_id: str):
    logger.info(f"Deleting task {task_id}")
    success = task_store.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"success": True}


agent_router = APIRouter(tags=["Agent"], prefix="/agent")


@agent_router.post("/revision", response_model=RevisionResponse)
async def generate_revision(request: RevisionRequest):
    logger.info(f"Generating revision schedule: subject={request.subject}")
    result = revision_agent.generate_revision_schedule(
        subject=request.subject,
        recent_tasks=request.recent_tasks,
        current_readiness=request.current_readiness
    )
    return RevisionResponse(success=True, data=result)


@agent_router.post("/replan", response_model=ReplanningResponse)
async def generate_replan(request: ReplanningRequest):
    logger.info("Generating replan")
    result = replanning_agent.generate_replan(
        current_tasks=request.current_tasks,
        missed_tasks=request.missed_tasks,
        new_availability=request.new_availability,
        readiness_change=request.readiness_change
    )
    return ReplanningResponse(success=True, data=result)


@agent_router.get("/insights", response_model=InsightResponse)
@agent_router.post("/insights", response_model=InsightResponse)
async def get_insights(request: InsightRequest = InsightRequest()):
    logger.info("Generating insights")
    result = insight_agent.generate_insights(request.student_data)
    return InsightResponse(success=True, data=result)


@agent_router.post("/student-analysis", response_model=StudentAnalysisResponse)
async def student_analysis(request: StudentAnalysisRequest):
    logger.info("Generating student analysis")
    analysis_data = {
        "strengths": ["Polity", "Current Affairs"],
        "weaknesses": request.student_data.get("weak_subjects", ["Geography", "Economics"]) if request.student_data else ["Geography", "Economics"],
        "improvement_areas": ["Time Management", "Revision"],
        "recommendations": ["Focus on Geography", "Take weekly mock tests"],
        "readiness_trend": "improving"
    }
    return StudentAnalysisResponse(
        success=True,
        data=analysis_data
    )


@agent_router.get("/status", response_model=AgentsStatusResponse)
async def get_agents_status():
    logger.info("Getting agents status")
    agents = [
        AgentStatus(name="Research Agent", status="active", last_run="2024-01-01T10:00:00", success_rate=0.95),
        AgentStatus(name="Planning Agent", status="active", last_run="2024-01-01T10:30:00", success_rate=0.98),
        AgentStatus(name="Revision Agent", status="idle", last_run="2024-01-01T09:00:00", success_rate=0.92),
        AgentStatus(name="Replanning Agent", status="idle", last_run="2024-01-01T08:00:00", success_rate=0.90),
        AgentStatus(name="Insight Agent", status="active", last_run="2024-01-01T11:00:00", success_rate=0.97)
    ]
    return AgentsStatusResponse(
        success=True,
        data=agents
    )


@agent_router.post("/workflow/run", response_model=WorkflowStatusResponse)
async def run_workflow(request: WorkflowRunRequest = WorkflowRunRequest()):
    logger.info("Running full workflow")
    result = orchestration_manager.run_full_workflow(request.context)
    return WorkflowStatusResponse(success=True, data=result)


@agent_router.get("/workflow/status", response_model=WorkflowStatusResponse)
async def get_workflow_status():
    logger.info("Getting workflow status")
    result = orchestration_manager.get_workflow_status()
    return WorkflowStatusResponse(success=True, data=result)


@agent_router.get("/orchestration/validate", response_model=WorkflowStatusResponse)
async def validate_orchestration():
    logger.info("Validating orchestration")
    result = orchestration_manager.validate_orchestration()
    return WorkflowStatusResponse(success=True, data=result)

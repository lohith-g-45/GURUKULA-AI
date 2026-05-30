
from fastapi import APIRouter, HTTPException
from app.schemas.tasks import (
    Task, TaskCreate, TaskUpdate, TaskListResponse, TaskResponse,
    RevisionRequest, RevisionResponse, ReplanningRequest, ReplanningResponse,
    InsightRequest, InsightResponse, WorkflowStatusResponse, WorkflowRunRequest
)
from app.schemas.common import StudentAnalysisRequest, StudentAnalysisResponse, AgentsStatusResponse, AgentStatus
from app.database.task_store import task_store
from app.database.agent_output_store import agent_output_cache
from app.database.user_store import user_profile_store, study_session_store, mock_score_store
from app.services.data_loader import DataLoader
from app.services.llm_service import LLMService
from app.utils.logger import logger
import time

router = APIRouter(tags=["Tasks"], prefix="/tasks")

data_loader = DataLoader()
llm_service = LLMService()


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
    start_time = time.time()
    logger.info(f"Generating revision schedule: subject={request.subject}, refresh={request.refresh}")
    
    try:
        tasks = task_store.get_all_tasks()
        
        context_for_cache = {
            "subject": request.subject,
            "tasks_completed_count": len([t for t in tasks if t.status == "completed"])
        }
        
        if not request.refresh:
            cached = agent_output_cache.get("revision", context_for_cache)
            if cached:
                logger.info("Returning cached revision schedule")
                return RevisionResponse(
                    success=True,
                    data=cached,
                    usage={},
                    cached=True
                )
        
        logger.info("Generating fresh revision schedule")
        
        all_data = data_loader.load_all()
        prompts = all_data.get("prompts", {})
        
        user_profile = user_profile_store.get_profile()
        weak_subjects = user_profile_store.get_weak_subjects()
        subject_weightage = all_data.get("analytics", {}).get("kas_subject_weightage", {})
        
        context_data = {
            "request": {
                "subject": request.subject,
                "recent_tasks": request.recent_tasks,
                "current_readiness": request.current_readiness
            },
            "user_profile": user_profile,
            "weak_subjects": weak_subjects,
            "subject_weightage": subject_weightage
        }
        
        llm_result = await llm_service.generate(
            prompt=prompts.get("revision_prompt", ""),
            context=context_data,
            system_instruction="You are a specialized KAS exam revision agent. Create a detailed, data-driven revision plan. Always respond with valid JSON."
        )
        
        if not llm_result.get("success"):
            raise Exception(f"LLM generation failed: {llm_result.get('error')}")
        
        agent_output_cache.set("revision", llm_result["data"], context_for_cache)
        
        return RevisionResponse(
            success=True,
            data=llm_result["data"],
            usage=llm_result.get("usage", {}),
            cached=False
        )
        
    except Exception as e:
        logger.error(f"Revision request failed: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to generate revision plan: {str(e)}")


@agent_router.post("/replan", response_model=ReplanningResponse)
async def generate_replan(request: ReplanningRequest):
    start_time = time.time()
    logger.info(f"Generating replan, refresh={request.refresh}")
    
    try:
        tasks = task_store.get_all_tasks()
        
        context_for_cache = {
            "missed_tasks_count": len(request.missed_tasks or []),
            "readiness_change": request.readiness_change
        }
        
        if not request.refresh:
            cached = agent_output_cache.get("replan", context_for_cache)
            if cached:
                logger.info("Returning cached replan")
                return ReplanningResponse(
                    success=True,
                    data=cached,
                    usage={},
                    cached=True
                )
        
        logger.info("Generating fresh replan")
        
        all_data = data_loader.load_all()
        prompts = all_data.get("prompts", {})
        planning_rules = all_data.get("planning", {})
        
        roadmap_rules = planning_rules.get("roadmap_rules", {})
        study_rules = planning_rules.get("study_planning_rules", {})
        
        context_data = {
            "request": {
                "current_tasks": request.current_tasks,
                "missed_tasks": request.missed_tasks,
                "new_availability": request.new_availability,
                "readiness_change": request.readiness_change
            },
            "roadmap_rules": roadmap_rules,
            "study_rules": study_rules
        }
        
        insight_prompt = prompts.get("insight_prompt", prompts.get("planning_prompt", ""))
        
        llm_result = await llm_service.generate(
            prompt=insight_prompt,
            context=context_data,
            system_instruction="You are a specialized KAS exam replanning agent. Analyze current situation and generate revised plan. Always respond with valid JSON."
        )
        
        if not llm_result.get("success"):
            raise Exception(f"LLM generation failed: {llm_result.get('error')}")
        
        agent_output_cache.set("replan", llm_result["data"], context_for_cache)
        
        return ReplanningResponse(
            success=True,
            data=llm_result["data"],
            usage=llm_result.get("usage", {}),
            cached=False
        )
        
    except Exception as e:
        logger.error(f"Replanning request failed: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to generate replan: {str(e)}")


@agent_router.get("/insights", response_model=InsightResponse)
async def get_insights_get():
    logger.info("Generating insights (GET)")
    from app.agents.insight_agent import insight_agent
    result = insight_agent.generate_insights()
    return InsightResponse(success=True, data=result)

@agent_router.post("/insights", response_model=InsightResponse)
async def get_insights_post(request: InsightRequest = InsightRequest()):
    logger.info("Generating insights (POST)")
    from app.agents.insight_agent import insight_agent
    result = insight_agent.generate_insights(request.student_data)
    return InsightResponse(success=True, data=result)


@agent_router.post("/student-analysis", response_model=StudentAnalysisResponse)
async def student_analysis(request: StudentAnalysisRequest):
    start_time = time.time()
    logger.info(f"Generating student analysis, refresh={request.refresh}")
    
    try:
        from app.database.task_store import task_store
        
        tasks = task_store.get_all_tasks()
        mock_scores = mock_score_store.get_all_scores()
        profile = user_profile_store.get_profile()
        
        context_for_cache = {
            "tasks_completed_count": len([t for t in tasks if t.status == "completed"]),
            "mock_scores_count": len(mock_scores),
            "readiness_score": user_profile_store.get_readiness_score(),
            "weak_subjects": user_profile_store.get_weak_subjects()
        }
        
        if not request.refresh:
            cached = agent_output_cache.get("student_analysis", context_for_cache)
            if cached:
                logger.info("Returning cached student analysis")
                return StudentAnalysisResponse(
                    success=True,
                    data=cached,
                    usage={},
                    cached=True
                )
        
        logger.info("Generating fresh student analysis")
        
        all_data = data_loader.load_all()
        prompts = all_data.get("prompts", {})
        
        completed_tasks = [t for t in tasks if t.status == "completed"]
        completion_rate = (len(completed_tasks) / len(tasks) * 100) if tasks else 0
        
        user_data = {
            "user_profile": profile,
            "weak_subjects": user_profile_store.get_weak_subjects(),
            "total_tasks": len(tasks),
            "completed_tasks": len(completed_tasks),
            "completion_rate": completion_rate,
            "mock_scores": mock_scores,
            "readiness_score": user_profile_store.get_readiness_score()
        }
        
        subject_weightage = all_data.get("analytics", {}).get("kas_subject_weightage", {})
        
        context_data = {
            "user_data": user_data,
            "subject_weightage": subject_weightage
        }
        
        llm_result = await llm_service.generate(
            prompt=prompts.get("student_analysis_prompt", ""),
            context=context_data,
            system_instruction="You are a specialized KAS exam student analysis agent. Analyze user performance. Always respond with valid JSON only in the exact format specified in the prompt."
        )
        
        if not llm_result.get("success"):
            raise Exception(f"LLM generation failed: {llm_result.get('error')}")
        
        # Save the new readiness score to user profile
        new_readiness = llm_result["data"].get("readiness_score")
        if new_readiness is not None:
            user_profile_store.update_profile({"readiness_score": new_readiness})
        
        agent_output_cache.set("student_analysis", llm_result["data"], context_for_cache)
        
        return StudentAnalysisResponse(
            success=True,
            data=llm_result["data"],
            usage=llm_result.get("usage", {}),
            cached=False
        )
        
    except Exception as e:
        logger.error(f"Student analysis request failed: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to generate student analysis: {str(e)}")


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
    from app.orchestration.orchestration_manager import orchestration_manager
    result = orchestration_manager.run_full_workflow(request.context)
    return WorkflowStatusResponse(success=True, data=result)


@agent_router.get("/workflow/status", response_model=WorkflowStatusResponse)
async def get_workflow_status():
    logger.info("Getting workflow status")
    from app.orchestration.orchestration_manager import orchestration_manager
    result = orchestration_manager.get_workflow_status()
    return WorkflowStatusResponse(success=True, data=result)


@agent_router.get("/orchestration/validate", response_model=WorkflowStatusResponse)
async def validate_orchestration():
    logger.info("Validating orchestration")
    from app.orchestration.orchestration_manager import orchestration_manager
    result = orchestration_manager.validate_orchestration()
    return WorkflowStatusResponse(success=True, data=result)

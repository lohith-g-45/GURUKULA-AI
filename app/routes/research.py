
from fastapi import APIRouter, HTTPException
from app.schemas.research import (
    ResearchRequest, ResearchResponse,
    StudentAnalysisRequest, StudentAnalysisResponse
)
from app.services.data_loader import DataLoader
from app.services.llm_service import LLMService
from app.database.agent_output_store import agent_output_cache
from app.database.user_store import user_profile_store, study_session_store, mock_score_store
from app.database.task_store import task_store
from app.utils.logger import logger
import time

router = APIRouter(tags=["Research & Student Analysis"], prefix="/agent")

data_loader = DataLoader()
llm_service = LLMService()


@router.post("/research", response_model=ResearchResponse)
async def get_research_insights(request: ResearchRequest = ResearchRequest(exam="KAS")):
    start_time = time.time()
    logger.info(f"Received research request for exam: {request.exam}, refresh={request.refresh}")
    
    try:
        context_for_cache = {"exam": request.exam}
        
        if not request.refresh:
            cached = agent_output_cache.get("research", context_for_cache)
            if cached:
                logger.info("Returning cached research insights")
                response_time_ms = round((time.time() - start_time) * 1000, 2)
                return ResearchResponse(
                    success=True,
                    data=cached,
                    usage={},
                    cached=True
                )
        
        logger.info("Generating fresh research insights")
        
        all_data = data_loader.load_all()
        prompts = all_data.get("prompts", {})
        
        subject_weightage = all_data.get("analytics", {}).get("kas_subject_weightage", {})
        topic_frequency = all_data.get("analytics", {}).get("kas_topic_frequency", {})
        
        optimized_topics = []
        if topic_frequency and topic_frequency.get("topics"):
            sorted_topics = sorted(
                topic_frequency["topics"].items(),
                key=lambda x: x[1],
                reverse=True
            )
            optimized_topics = [{"topic": k, "frequency": v} for k, v in sorted_topics[:20]]
        
        context_data = {
            "exam": request.exam,
            "subject_weightage": subject_weightage,
            "top_topics": optimized_topics
        }
        
        llm_result = await llm_service.generate(
            prompt=prompts.get("research_prompt", ""),
            context=context_data,
            system_instruction="You are a specialized KAS exam research agent. Always respond with valid JSON."
        )
        
        if not llm_result.get("success"):
            raise Exception(f"LLM generation failed: {llm_result.get('error')}")
        
        agent_output_cache.set("research", llm_result["data"], context_for_cache)
        
        return ResearchResponse(
            success=True,
            data=llm_result["data"],
            usage=llm_result.get("usage", {}),
            cached=False
        )
        
    except Exception as e:
        logger.error(f"Research request failed: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to generate research insights: {str(e)}")


@router.post("/student-analysis", response_model=StudentAnalysisResponse)
async def get_student_analysis(request: StudentAnalysisRequest = StudentAnalysisRequest()):
    start_time = time.time()
    logger.info(f"Received student analysis request, refresh={request.refresh}")
    
    try:
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

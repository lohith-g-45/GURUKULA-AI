
from fastapi import APIRouter, HTTPException
from app.schemas.planning import PlanningRequest, PlanningResponse
from app.services.data_loader import DataLoader
from app.services.llm_service import LLMService
from app.database.agent_output_store import agent_output_cache
from app.database.user_store import user_profile_store
from app.utils.logger import logger
import time

router = APIRouter(tags=["Planning Agent"], prefix="/agent")

data_loader = DataLoader()
llm_service = LLMService()


@router.post("/planner", response_model=PlanningResponse)
async def get_planning(request: PlanningRequest = PlanningRequest()):
    start_time = time.time()
    logger.info(f"Received planning request, refresh={request.refresh}")
    
    try:
        profile_available_hours = user_profile_store.get_available_hours()
        profile_weak_subjects = user_profile_store.get_weak_subjects()
        profile_readiness = user_profile_store.get_readiness_score()
        
        context_for_cache = {
            "readiness_score": request.readiness_score or profile_readiness,
            "available_hours_per_day": request.available_hours_per_day or profile_available_hours,
            "weak_subjects": request.weak_subjects or profile_weak_subjects
        }
        
        if not request.refresh:
            cached = agent_output_cache.get("planning", context_for_cache)
            if cached:
                logger.info("Returning cached planning")
                return PlanningResponse(
                    success=True,
                    data=cached,
                    usage={},
                    cached=True
                )
        
        logger.info("Generating fresh planning")
        
        all_data = data_loader.load_all()
        prompts = all_data.get("prompts", {})
        planning_rules = all_data.get("planning", {})
        
        subject_weightage = all_data.get("analytics", {}).get("kas_subject_weightage", {})
        roadmap_rules = planning_rules.get("roadmap_rules", {})
        study_rules = planning_rules.get("study_planning_rules", {})
        revision_rules = planning_rules.get("revision_cycles", {})
        mock_rules = planning_rules.get("mock_planning_rules", {})
        
        # Optimize subject weightage: keep only top 5, minimal fields
        if "subjects" in subject_weightage:
            subjects_list = list(subject_weightage["subjects"].items())
            subjects_list.sort(key=lambda x: (
                {"Very High": 0, "High": 1, "Medium": 2, "Low": 3}.get(x[1].get("priority", "Medium")),
                -x[1].get("frequency_score", 0)
            ))
            top_subjects = dict(subjects_list[:3])  # Only top 3 instead of 5
            optimized_subjects = {}
            for name, data in top_subjects.items():
                optimized_subjects[name] = {
                    "prelims": data.get("prelims_weightage"),
                    "mains": data.get("mains_weightage"),
                    "prio": data.get("priority")
                }
            subject_weightage = {"subjects": optimized_subjects}  # Remove 'exam' field

        # Simplify roadmap rules even further
        optimized_roadmap = {
            "phases": roadmap_rules.get("roadmap_generation_logic", {}).get("phase_names", []),
            "phase_weeks": roadmap_rules.get("roadmap_generation_logic", {}).get("phase_duration_weeks", {}),
            "min_days": roadmap_rules.get("weekly_planning_rules", {}).get("min_study_days_per_week", 5),
            "default_hours": roadmap_rules.get("weekly_planning_rules", {}).get("default_daily_hours", 6)
        }

        # Simplify study rules
        optimized_study = {
            "subject_order": study_rules.get("daily_study_distribution_rules", {}).get("subject_priority_order", []),
            "max_subjects_day": study_rules.get("daily_study_distribution_rules", {}).get("max_subjects_per_day", 3)
        }

        # Simplify revision and mock rules
        optimized_revision = {"intervals": revision_rules.get("spaced_repetition_intervals", [])[:3]}  # Only first 3
        optimized_mock = {"freq": mock_rules.get("mock_frequency_rules", {}).get("exam_distance_factors", {})}

        context_data = {
            "req": {
                "readiness": request.readiness_score,
                "hours": request.available_hours_per_day,
                "weak": request.weak_subjects,
                "exam": request.exam
            },
            "roadmap": optimized_roadmap,
            "study": optimized_study,
            "revision": optimized_revision,
            "mock": optimized_mock,
            "weights": subject_weightage
        }
        
        llm_result = await llm_service.generate(
            prompt=prompts.get("planning_prompt", ""),
            context=context_data,
            system_instruction="You are a specialized KAS exam planning agent. Create a detailed, data-driven study plan. Always respond with valid JSON."
        )
        
        if not llm_result.get("success"):
            raise Exception(f"LLM generation failed: {llm_result.get('error')}")
        
        agent_output_cache.set("planning", llm_result["data"], context_for_cache)
        
        return PlanningResponse(
            success=True,
            data=llm_result["data"],
            usage=llm_result.get("usage", {}),
            cached=False
        )
        
    except Exception as e:
        logger.error(f"Planning request failed: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to generate plan: {str(e)}")

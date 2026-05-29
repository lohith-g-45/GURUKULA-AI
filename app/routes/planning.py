
from fastapi import APIRouter
from app.schemas.planning import PlanningRequest, PlanningResponse
from app.services.data_loader import DataLoader
from app.services.llm_service import LLMService
from app.utils.logger import logger

router = APIRouter(tags=["Planning Agent"], prefix="/agent")

data_loader = DataLoader()
llm_service = LLMService()

# Minimal prompt to save tokens
MINIMAL_PLANNING_PROMPT = """Generate a JSON KAS study plan with:
- preparation_roadmap
- subject_plan
- weekly_schedule
- daily_schedule
- milestones
- revision_cycles
- mock_schedule
Only JSON, no extra text."""

def generate_fallback_plan(request: PlanningRequest, all_data) -> dict:
    """Generate a fallback plan using actual datasets when LLM fails!"""
    planning_data = all_data.get("planning", {})
    roadmap_rules = planning_data.get("roadmap_rules", {})
    study_rules = planning_data.get("study_planning_rules", {})
    revision_data = planning_data.get("revision_cycles", {})
    mock_rules = planning_data.get("mock_planning_rules", {})
    micro_milestones = planning_data.get("micro_milestone_rules", {})

    phase_names = roadmap_rules.get("roadmap_generation_logic", {}).get("phase_names", ["Foundation", "Core Concepts", "Advanced & Practice", "Revision & Mock Tests"])
    subject_priority = study_rules.get("daily_study_distribution_rules", {}).get("subject_priority_order", [])
    revision_subjects = list(revision_data.get("subject_revision_priority", {}).keys())

    # Build fallback plan
    fallback_plan = {
        "preparation_roadmap": {
            "duration_months": 6,
            "stages": [
                {
                    "stage_name": phase,
                    "duration_weeks": 4 if phase == "Foundation" else 6 if phase == "Revision & Mock Tests" else 5,
                    "focus_subjects": subject_priority[:3],
                    "weekly_hours": request.available_hours_per_day * 6
                }
                for phase in phase_names
            ]
        },
        "subject_plan": [
            {
                "subject": subj,
                "priority": "High" if idx < 3 else "Medium",
                "allocated_hours": 100 - (idx * 5),
                "topics": [{"name": f"{subj} Topic 1", "hours": 20, "priority": "High"}]
            }
            for idx, subj in enumerate(subject_priority)
        ],
        "weekly_schedule": {
            "daily_targets": ["Complete daily topic", "Solve 50 MCQs"],
            "mock_test_frequency": "Weekly",
            "study_days_per_week": 6,
            "daily_hours": request.available_hours_per_day
        },
        "daily_schedule": [
            {
                "day": day,
                "items": [
                    {"time_slot": "6:00 AM - 8:00 AM", "subject": subject_priority[0], "activity": "Concept Learning"},
                    {"time_slot": "8:00 AM - 9:30 AM", "subject": subject_priority[1], "activity": "MCQ Practice"},
                    {"time_slot": "4:00 PM - 6:00 PM", "subject": subject_priority[2], "activity": "Revision"}
                ]
            }
            for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        ],
        "milestones": [
            {"description": "Complete Foundation Phase", "criteria": ["All foundation topics done"], "reward": "+15 points", "target_stage": "Foundation"},
            {"description": "Finish Core Concepts", "criteria": ["All core topics done"], "reward": "+20 points", "target_stage": "Core Concepts"},
            {"description": "Solve 500+ MCQs", "criteria": ["500 MCQs solved"], "reward": "+10 points", "target_stage": "Advanced & Practice"},
            {"description": "First Full Mock", "criteria": ["Mock test taken"], "reward": "+10 points", "target_stage": "Revision & Mock Tests"},
            {"description": "Exam Ready", "criteria": ["All revisions done"], "reward": "Exam Ready", "target_stage": "Revision & Mock Tests"}
        ],
        "revision_cycles": [
            {
                "subject": subj,
                "revision_days": revision_data.get("spaced_repetition_intervals", [1,3,7,14]),
                "priority_score": revision_data.get("subject_revision_priority", {}).get(subj, {}).get("priority_score", 10),
                "revision_frequency": revision_data.get("subject_revision_priority", {}).get(subj, {}).get("revision_frequency", "Weekly")
            }
            for subj in revision_subjects
        ],
        "mock_schedule": {
            "mock_type": "Full-Length Mocks" if request.readiness_score > 70 else "Sectional Mocks",
            "frequency": "Weekly",
            "focus_subjects": subject_priority[:5],
            "post_mock_analysis": True
        }
    }
    return fallback_plan

@router.post("/planner", response_model=PlanningResponse)
async def get_planning(request: PlanningRequest = PlanningRequest()):
    logger.info(f"Received planning request: readiness={request.readiness_score}, daily_hours={request.available_hours_per_day}")
    
    all_data = data_loader.load_all()
    
    # Try LLM first with minimal prompt and tiny context!
    try:
        tiny_context = {
            "r": request.readiness_score,
            "h": request.available_hours_per_day,
            "d": request.exam_date_distance_days,
            "w": request.weak_subjects
        }
        result = await llm_service.generate(
            prompt=MINIMAL_PLANNING_PROMPT,
            context=tiny_context,
            schema=None
        )
        if result["success"]:
            logger.info("LLM plan generated successfully!")
            return PlanningResponse(
                success=True,
                data=result["data"],
                usage=result.get("usage", {})
            )
    except Exception as e:
        logger.warning(f"LLM generation failed, falling back: {str(e)}")
    
    # If LLM failed (rate limit, etc.), use fallback plan!
    logger.info("Using fallback plan generation!")
    fallback_data = generate_fallback_plan(request, all_data)
    return PlanningResponse(
        success=True,
        data=fallback_data,
        usage={}
    )


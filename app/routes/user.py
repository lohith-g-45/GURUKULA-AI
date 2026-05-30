
from fastapi import APIRouter
from app.schemas.common import UserProfileRequest, UserProfileResponse
from app.database.user_store import user_profile_store
from app.agents.task_agent import task_generation_engine
from app.utils.logger import logger


router = APIRouter(tags=["User"], prefix="/user")


@router.get("/profile", response_model=UserProfileResponse)
async def get_user_profile():
    logger.info("Fetching user profile")
    profile = user_profile_store.get_profile()
    return UserProfileResponse(
        success=True,
        message="Profile retrieved successfully",
        data=profile
    )


@router.post("/profile", response_model=UserProfileResponse)
async def update_user_profile(request: UserProfileRequest):
    logger.info(f"Received user profile update")
    profile_data = {
        "name": request.name or "Student",
        "email": request.email or "student@example.com",
        "exam": request.exam,
        "readiness_score": request.readiness_score,
        "available_hours_per_day": request.available_hours_per_day,
        "weak_subjects": request.weak_subjects,
        "study_goals": request.study_goals
    }
    updated = user_profile_store.update_profile(profile_data)
    try:
        task_generation_engine.generate_initial_tasks()
    except Exception as e:
        logger.warning(f"Could not generate initial tasks: {e}")
    return UserProfileResponse(
        success=True,
        message="Profile updated successfully",
        data=updated
    )


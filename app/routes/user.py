
from fastapi import APIRouter
from app.schemas.common import UserProfileRequest, UserProfileResponse
from app.utils.logger import logger


router = APIRouter(tags=["User"], prefix="/user")


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
    return UserProfileResponse(
        success=True,
        message="Profile updated successfully",
        data=profile_data
    )



import asyncio
from app.routes.planning import generate_fallback_plan
from app.schemas.planning import PlanningRequest
from app.services.data_loader import DataLoader

async def test_fallback_plan():
    print("="*80)
    print("TESTING FALLBACK PLAN GENERATION")
    print("="*80)
    
    test_request = PlanningRequest(
        exam="KAS",
        readiness_score=70.0,
        available_hours_per_day=6.0,
        exam_date_distance_days=180,
        weak_subjects=["History", "Geography"]
    )
    
    data_loader = DataLoader()
    all_data = data_loader.load_all()
    
    print("Generating fallback plan...")
    fallback_plan = generate_fallback_plan(test_request, all_data)
    
    # Validate all required sections are present!
    required_sections = [
        "preparation_roadmap",
        "subject_plan",
        "weekly_schedule",
        "daily_schedule",
        "milestones",
        "revision_cycles",
        "mock_schedule"
    ]
    all_valid = True
    for section in required_sections:
        if section not in fallback_plan:
            print(f"[FAIL] MISSING SECTION: {section}")
            all_valid = False
        else:
            if isinstance(fallback_plan[section], list) and len(fallback_plan[section]) == 0:
                print(f"[FAIL] EMPTY LIST SECTION: {section}")
                all_valid = False
            else:
                print(f"[OK] VALID SECTION: {section}")
    
    print("="*80)
    if all_valid:
        print("[SUCCESS] FALLBACK PLAN VALID - ALL SECTIONS PRESENT!")
        print(f"PREPARATION ROADMAP: {len(fallback_plan['preparation_roadmap']['stages'])} phases")
        print(f"SUBJECT PLAN: {len(fallback_plan['subject_plan'])} subjects")
        print(f"DAILY SCHEDULE: {len(fallback_plan['daily_schedule'])} days")
        print(f"MILESTONES: {len(fallback_plan['milestones'])} items")
        print(f"REVISION CYCLES: {len(fallback_plan['revision_cycles'])} subjects")
        print(f"MOCK SCHEDULE: {fallback_plan['mock_schedule']['mock_type']}")
    else:
        print("[FAIL] FALLBACK PLAN INVALID!")
    print("="*80)

if __name__ == "__main__":
    asyncio.run(test_fallback_plan())

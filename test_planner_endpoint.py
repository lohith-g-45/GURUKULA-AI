
import httpx
import json

BASE_URL = "http://localhost:8000/api/v1"

print("=== Testing Planner Endpoint ===")

# Create a user profile first for test
test_profile = {
    "name": "Test User",
    "email": "test@example.com",
    "exam": "KAS",
    "available_hours_per_day": 6,
    "exam_date_distance_days": 180,
    "weak_subjects": ["History", "English"],
    "readiness_score": 70,
    "goals": ["Complete syllabus", "Take mock tests"]
}

try:
    print("\n1. Sending test profile...")
    response = httpx.post(f"{BASE_URL}/user/profile", json=test_profile, timeout=60)
    print(f"   Status: {response.status_code}")

    print("\n2. Sending planner request...")
    planner_payload = {
        "exam": "KAS",
        "readiness_score": 70,
        "available_hours_per_day": 6,
        "exam_date_distance_days": 180,
        "weak_subjects": ["History", "English"],
        "refresh": True
    }
    planner_response = httpx.post(f"{BASE_URL}/agent/planner", json=planner_payload, timeout=60)
    print(f"   Status: {planner_response.status_code}")
    if planner_response.status_code == 200:
        print("   Planner Response:")
        print(json.dumps(planner_response.json(), indent=2))
    else:
        print("   Error Response:")
        print(planner_response.text)
except Exception as e:
    print(f"\nException: {type(e)} - {e}")
    import traceback
    traceback.print_exc()


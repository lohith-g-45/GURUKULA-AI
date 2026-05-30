
import httpx
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_health():
    print("=== Testing /health ===")
    response = httpx.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    return response.status_code == 200

def test_user_profile():
    print("=== Testing POST /user/profile ===")
    payload = {
        "name": "Test User",
        "email": "test@example.com",
        "exam": "KAS",
        "available_hours_per_day": 6,
        "exam_date_distance_days": 180,
        "weak_subjects": ["History", "English"],
        "readiness_score": 70,
        "goals": ["Complete syllabus", "Take mock tests"]
    }
    response = httpx.post(f"{BASE_URL}/user/profile", json=payload)
    print(f"Status: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    except Exception as e:
        print(f"Response: {response.text}\n")
    return response.status_code == 200

def test_agent_research():
    print("=== Testing POST /agent/research ===")
    payload = {"exam": "KAS", "refresh": False}
    response = httpx.post(f"{BASE_URL}/agent/research", json=payload)
    print(f"Status: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    except Exception as e:
        print(f"Response: {response.text}\n")
    return response.status_code == 200

def test_student_analysis():
    print("=== Testing POST /agent/student-analysis ===")
    payload = {"refresh": False}
    response = httpx.post(f"{BASE_URL}/agent/student-analysis", json=payload)
    print(f"Status: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    except Exception as e:
        print(f"Response: {response.text}\n")
    return response.status_code == 200

def test_planner():
    print("=== Testing POST /agent/planner ===")
    payload = {
        "exam": "KAS",
        "readiness_score": 70,
        "available_hours_per_day": 6,
        "exam_date_distance_days": 180,
        "weak_subjects": ["History", "English"],
        "refresh": False
    }
    response = httpx.post(f"{BASE_URL}/agent/planner", json=payload)
    print(f"Status: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    except Exception as e:
        print(f"Response: {response.text}\n")
    return response.status_code == 200

def test_revision():
    print("=== Testing POST /agent/revision ===")
    payload = {"subject": "History", "refresh": False}
    response = httpx.post(f"{BASE_URL}/agent/revision", json=payload)
    print(f"Status: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    except Exception as e:
        print(f"Response: {response.text}\n")
    return response.status_code == 200

def test_replan():
    print("=== Testing POST /agent/replan ===")
    payload = {"readiness_change": -5, "refresh": False}
    response = httpx.post(f"{BASE_URL}/agent/replan", json=payload)
    print(f"Status: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    except Exception as e:
        print(f"Response: {response.text}\n")
    return response.status_code == 200

def test_dashboard():
    print("=== Testing GET /dashboard ===")
    response = httpx.get(f"{BASE_URL}/dashboard")
    print(f"Status: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    except Exception as e:
        print(f"Response: {response.text}\n")
    return response.status_code == 200

if __name__ == "__main__":
    results = []
    results.append(("Health", test_health()))
    results.append(("POST /user/profile", test_user_profile()))
    results.append(("POST /agent/research", test_agent_research()))
    results.append(("POST /agent/student-analysis", test_student_analysis()))
    results.append(("POST /agent/planner", test_planner()))
    results.append(("POST /agent/revision", test_revision()))
    results.append(("POST /agent/replan", test_replan()))
    results.append(("GET /dashboard", test_dashboard()))
    
    print("\n=== Summary ===")
    print("Endpoint | Status | Success")
    print("---------|--------|--------")
    for name, success in results:
        status = "OK" if success else "FAILED"
        print(f"{name:25s} | {status:6s} | {success}")

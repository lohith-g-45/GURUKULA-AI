
import requests
import json

BASE_URL = "http://localhost:8000"

def test_docs():
    print("\n=== Testing /docs ===")
    try:
        response = requests.get(f"{BASE_URL}/docs")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("[OK] /docs OK!")
        else:
            print(f"[FAIL] /docs failed with status {response.status_code}")
    except Exception as e:
        print(f"[FAIL] /docs failed: {e}")

def test_dashboard():
    print("\n=== Testing /api/v1/dashboard ===")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/dashboard")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("[OK] Dashboard API OK!")
            print("Response:", json.dumps(response.json(), indent=2))
        else:
            print(f"[FAIL] Dashboard API failed with status {response.status_code}")
            print("Response:", response.text)
    except Exception as e:
        print(f"[FAIL] Dashboard API failed: {e}")

def test_tasks():
    print("\n=== Testing /api/v1/tasks ===")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/tasks")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("[OK] Tasks API OK!")
            print("Response:", json.dumps(response.json(), indent=2))
        else:
            print(f"[FAIL] Tasks API failed with status {response.status_code}")
            print("Response:", response.text)
    except Exception as e:
        print(f"[FAIL] Tasks API failed: {e}")

def test_student_analysis():
    print("\n=== Testing /api/v1/agent/student-analysis ===")
    try:
        data = {"refresh": False}
        response = requests.post(f"{BASE_URL}/api/v1/agent/student-analysis", json=data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("[OK] Student Analysis API OK!")
            print("Response:", json.dumps(response.json(), indent=2))
        else:
            print(f"[FAIL] Student Analysis API failed with status {response.status_code}")
            print("Response:", response.text)
    except Exception as e:
        print(f"[FAIL] Student Analysis API failed: {e}")

def test_planner():
    print("\n=== Testing /api/v1/agent/planner ===")
    try:
        data = {"refresh": False, "readiness_score": 70, "available_hours_per_day": 6}
        response = requests.post(f"{BASE_URL}/api/v1/agent/planner", json=data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("[OK] Planner API OK!")
            print("Response:", json.dumps(response.json(), indent=2))
        else:
            print(f"[FAIL] Planner API failed with status {response.status_code}")
            print("Response:", response.text)
    except Exception as e:
        print(f"[FAIL] Planner API failed: {e}")

if __name__ == "__main__":
    print("Starting Phase 5 Validation...")
    test_docs()
    test_dashboard()
    test_tasks()
    test_student_analysis()
    test_planner()
    print("\n=== Phase 5 Validation Complete! ===")

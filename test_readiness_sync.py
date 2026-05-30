
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"


def test_dashboard():
    print("=== Testing Dashboard Endpoint ===")
    try:
        res = requests.get(f"{BASE_URL}/dashboard")
        print(f"Status: {res.status_code}")
        data = res.json()
        print(f"Dashboard readiness: {data['data']['readiness_score']}")
        return data['data']['readiness_score']
    except Exception as e:
        print(f"Dashboard test failed: {e}")
        return None


def test_student_analysis():
    print("\n=== Testing Student Analysis Endpoint ===")
    try:
        res = requests.post(f"{BASE_URL}/agent/student-analysis", json={"refresh": True})
        print(f"Status: {res.status_code}")
        data = res.json()
        print(f"Student analysis readiness: {data['data']['readiness_score']}")
        print(f"Student analysis perf summary readiness: {data['data']['performance_summary']['current_readiness']}")
        return data['data']['readiness_score']
    except Exception as e:
        print(f"Student analysis test failed: {e}")
        return None


def test_insights():
    print("\n=== Testing Insights Endpoint ===")
    try:
        res = requests.get(f"{BASE_URL}/agent/insights")
        print(f"Status: {res.status_code}")
        data = res.json()
        print(f"Insights readiness: {data['data']['performance_summary']['current_readiness']}")
        return data['data']['performance_summary']['current_readiness']
    except Exception as e:
        print(f"Insights test failed: {e}")
        return None


if __name__ == "__main__":
    print("Testing readiness sync across all endpoints")
    dashboard_readiness = test_dashboard()
    student_analysis_readiness = test_student_analysis()
    insights_readiness = test_insights()

    print("\n=== Final Results ===")
    print(f"Dashboard: {dashboard_readiness}")
    print(f"Student Analysis: {student_analysis_readiness}")
    print(f"Insights: {insights_readiness}")

    if dashboard_readiness == student_analysis_readiness == insights_readiness:
        print("\nREADINESS SYNC VERIFIED")
    else:
        print("\nREADINESS SYNC FAILED: Values are not the same")

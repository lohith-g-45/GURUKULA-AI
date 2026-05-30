
import sys
import time
from pathlib import Path
from typing import Dict, List

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def print_separator(title=""):
    print("\n" + "=" * 100)
    if title:
        print(f"  {title}")
        print("=" * 100)

def measure_endpoint(method: str, url: str, json_data: Dict = None) -> Dict:
    """Measure endpoint response time and return results."""
    start = time.time()
    try:
        if method.upper() == "GET":
            response = client.get(url)
        elif method.upper() == "POST":
            response = client.post(url, json=json_data or {})
        else:
            return {"error": "Invalid method"}
        
        duration = time.time() - start
        return {
            "url": url,
            "method": method,
            "status_code": response.status_code,
            "duration": round(duration, 4),
            "success": response.status_code == 200
        }
    except Exception as e:
        duration = time.time() - start
        return {
            "url": url,
            "method": method,
            "error": str(e),
            "duration": round(duration, 4),
            "success": False
        }


# --- PERFORMANCE AUDIT ---
print_separator("GURUKULA AI - PERFORMANCE AUDIT")

# Define test data
sample_user_data = {
    "name": "Test Student",
    "exam": "KAS",
    "readiness_score": 70,
    "available_hours_per_day": 6,
    "weak_subjects": ["Geography", "Economics"],
    "study_goals": ["Score 90%", "Complete revision"]
}
sample_revision = {
    "subject": "Polity",
    "current_readiness": 70
}
sample_replan = {
    "new_availability": 7,
    "readiness_change": -5
}

# Run measurements
print("\nMeasuring endpoints...")

# List of endpoints to measure
endpoints = [
    ("GET", "/api/v1/dashboard", None),
    ("POST", "/api/v1/agent/research", {"topic": "Indian Polity"}),
    ("POST", "/api/v1/agent/student-analysis", {"student_data": sample_user_data}),
    ("POST", "/api/v1/agent/revision", sample_revision),
    ("POST", "/api/v1/agent/replan", sample_replan),
    ("POST", "/api/v1/agent/planner", sample_user_data),
]

results = []
for method, url, data in endpoints:
    result = measure_endpoint(method, url, data)
    results.append(result)
    status = "SUCCESS" if result["success"] else "FAILED"
    print(f"  {result['method']} {result['url']} -> {result['duration']}s {status}")


# --- ANALYSIS ---
print_separator("ENDPOINT TIMINGS")
print(f"\n{'Endpoint':<40} {'Method':<10} {'Duration (s)':<15} {'Status':<10}")
print("-" * 90)

slow_endpoints = []
total_duration = 0.0
for r in results:
    duration = r["duration"]
    status = "OK" if r["success"] else "FAILED"
    print(f"{r['url']:<40} {r['method']:<10} {duration:<15} {status:<10}")
    total_duration += duration
    
    if duration > 2.0 and r["success"]:
        slow_endpoints.append(r)

print_separator("BOTTLENECKS")
if slow_endpoints:
    print("\nEndpoints taking > 2 seconds:")
    for r in slow_endpoints:
        print(f"  - {r['method']} {r['url']}: {r['duration']}s")
else:
    print("No slow endpoints found!")

print_separator("SUMMARY")
print(f"\nTotal time for all endpoints: {round(total_duration, 4)}s")
print(f"Number of endpoints: {len(results)}")
print(f"Average time per endpoint: {round(total_duration / len(results), 4)}s")


# --- CHECK FOR COMMON ISSUES ---
print_separator("CHECKING FOR COMMON PERFORMANCE ISSUES")
print("\nChecking backend source files for potential issues...")

# Check research agent
research_path = project_root / "app" / "agents" / "research_agent.py"
if research_path.exists():
    print("\nResearch agent:")
    with open(research_path, encoding="utf-8") as f:
        content = f.read()
        if "llm_service" in content:
            print("  - Uses LLM service (may be slow)")
        if "data_loader" in content:
            print("  - Uses data loader")

# Check frontend React Query usage
frontend_path = project_root / "frontend"
print("\nChecking frontend React Query usage...")
qclient_files = list(frontend_path.rglob("*.tsx"))
for f in qclient_files[:10]:
    if "react-query" in open(f, encoding="utf-8").read():
        print(f"  - Found React Query usage in {f.name}")

print_separator("PERFORMANCE AUDIT COMPLETE")


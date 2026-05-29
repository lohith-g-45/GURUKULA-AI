
import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def print_separator(title=""):
    print("\n" + "=" * 80)
    if title:
        print(f"  {title}")
        print("=" * 80)


print_separator("Testing FastAPI Endpoints")

# Test 1: Orchestration validation
print_separator("Test: /api/v1/agent/orchestration/validate")
response = client.get("/api/v1/agent/orchestration/validate")
print(f"Status code: {response.status_code}")
print(f"Response: {response.json()}")
assert response.status_code == 200
assert response.json()["success"] is True


# Test 2: Workflow run
print_separator("Test: POST /api/v1/agent/workflow/run")
response = client.post("/api/v1/agent/workflow/run", json={"context": {}})
print(f"Status code: {response.status_code}")
result = response.json()
print(f"Completed: {result['data']['completed']}")
print(f"Results count: {len(result['data']['results'])}")
for stage_result in result["data"]["results"]:
    print(f"  - {stage_result['stage']}: {'SUCCESS' if stage_result['success'] else 'FAILED'}")

assert response.status_code == 200
assert result["success"] is True
assert result["data"]["completed"] is True


# Test 3: Insights endpoint
print_separator("Test: GET /api/v1/agent/insights")
response = client.get("/api/v1/agent/insights")
print(f"Status code: {response.status_code}")
print(f"Has insights: {'insights' in response.json()['data']}")
assert response.status_code == 200
assert response.json()["success"] is True


print_separator("ALL ENDPOINT TESTS PASSED")
print("\n" + "*" * 80)
print("*" + " " * 78 + "*")
print("*" + " " * 25 + "PHASE 7 FULLY WORKING!" + " " * 31 + "*")
print("*" + " " * 78 + "*")
print("*" * 80)


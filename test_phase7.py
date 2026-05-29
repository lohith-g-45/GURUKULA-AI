
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.orchestration.orchestration_manager import orchestration_manager
from app.agents.insight_agent import insight_agent
from app.orchestration.context_store import context_store


def print_separator(title=""):
    print("\n" + "=" * 80)
    if title:
        print(f"  {title}")
        print("=" * 80)


print_separator("PHASE 7 TEST STARTING")

# Test 1: Validate orchestration
print_separator("Test 1: Orchestration Validation")
validation = orchestration_manager.validate_orchestration()
print(f"Validation result: {validation['valid']}")
for check in validation['checks']:
    print(f"  - {check['check']}: {check['status']}")
assert validation['valid'], "Orchestration validation failed!"


# Test 2: Context store functionality
print_separator("Test 2: Context Store")
context_store.set("test_key", "test_value")
print(f"Set test_key to: {context_store.get('test_key')}")
assert context_store.get("test_key") == "test_value"
context_store.update({"test_key2": "value2", "test_key3": 123})
print(f"Context store keys: {list(context_store.get_all().keys())}")
assert "test_key2" in context_store.get_all()
context_store.delete("test_key")
print(f"Deleted test_key, current keys: {list(context_store.get_all().keys())}")


# Test 3: Insight Agent
print_separator("Test 3: Insight Agent")
test_student_data = {
    "readiness_score": 65,
    "daily_study_hours": 11,
    "consecutive_study_days": 10,
    "subject_scores": {
        "Polity": 55,
        "History": 70,
        "Geography": 45,
        "Environment": 50
    }
}
insights = insight_agent.generate_insights(test_student_data)
print(f"Generated insights at: {insights.get('generated_at')}")
print(f"Burnout alerts: {len(insights.get('burnout_alerts', []))}")
print(f"Weak subjects: {len(insights.get('weak_subjects', []))}")
for weak in insights.get('weak_subjects', []):
    print(f"  - {weak['subject']}: {weak['score']}")
assert "burnout_alerts" in insights
assert "weak_subjects" in insights


# Test 4: Run full workflow
print_separator("Test 4: Full Workflow Execution")
workflow_context = {
    "student_data": test_student_data,
    "tasks": [
        {"id": "1", "title": "Test Task 1", "status": "completed"},
        {"id": "2", "title": "Test Task 2", "status": "pending"},
        {"id": "3", "title": "Test Task 3", "status": "missed"}
    ]
}
workflow_result = orchestration_manager.run_full_workflow(workflow_context)
print(f"Workflow completed: {workflow_result.get('completed')}")
print(f"Results count: {len(workflow_result.get('results', []))}")
for res in workflow_result.get('results', []):
    print(f"  - {res['stage']}: {'SUCCESS' if res['success'] else 'FAILED'}")


# Test 5: Workflow status
print_separator("Test 5: Workflow Status")
status = orchestration_manager.get_workflow_status()
print(f"Current stage: {status.get('current_stage')}")
print(f"History entries: {len(status.get('history', []))}")


print_separator("ALL TESTS PASSED")
print("\n" + "*" * 80)
print("*" + " " * 78 + "*")
print("*" + " " * 20 + "PHASE 7 COMPLETED SUCCESSFULLY!" + " " * 26 + "*")
print("*" + " " * 78 + "*")
print("*" * 80)


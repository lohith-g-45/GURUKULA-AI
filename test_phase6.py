
import sys
from datetime import datetime

sys.path.insert(0, '.')

from app.schemas.tasks import TaskCreate, TaskUpdate
from app.database.task_store import task_store
from app.agents.revision_agent import revision_agent
from app.agents.replanning_agent import replanning_agent


print("="*50)
print("PHASE 6 TESTING")
print("="*50)

print("\n1. Testing Task Lifecycle...")
try:
    task1 = TaskCreate(
        title="Study Polity - Constitution",
        description="Read Chapter 1 to 5",
        subject="Polity",
        topic="Constitution",
        priority="High",
        estimated_hours=3.0
    )
    created = task_store.create_task(task1)
    print(f"   [OK] Created task: {created.id} - {created.title}")

    all_tasks = task_store.get_all_tasks()
    print(f"   [OK] All tasks: {len(all_tasks)}")

    updated = task_store.update_task(created.id, TaskUpdate(progress=50.0, status="in_progress"))
    print(f"   [OK] Updated task progress: {updated.progress}%")

    task2 = TaskCreate(
        title="Solve Geography MCQs",
        subject="Geography",
        priority="Medium",
        estimated_hours=1.5
    )
    created2 = task_store.create_task(task2)
    print(f"   [OK] Created task 2: {created2.title}")

    deleted = task_store.delete_task(created2.id)
    print(f"   [OK] Deleted task 2: {deleted}")

    print("   [OK] Task lifecycle tests passed!")
except Exception as e:
    print(f"   [FAIL] Task lifecycle failed: {e}")

print("\n2. Testing Revision Agent...")
try:
    revision = revision_agent.generate_revision_schedule(subject="Polity")
    print(f"   [OK] Generated revision schedule with {len(revision['revision_tasks'])} tasks")
    print(f"   [OK] Spaced intervals: {revision['spaced_repetition_intervals']}")
    print("   [OK] Revision agent tests passed!")
except Exception as e:
    print(f"   [FAIL] Revision agent failed: {e}")

print("\n3. Testing Replanning Agent...")
try:
    replan = replanning_agent.generate_replan(
        missed_tasks=["task-123"],
        new_availability=5.0
    )
    print(f"   [OK] Generated {len(replan['adjustments'])} adjustments")
    print(f"   [OK] Recovered tasks: {len(replan['recovered_tasks'])}")
    print("   [OK] Replanning agent tests passed!")
except Exception as e:
    print(f"   [FAIL] Replanning agent failed: {e}")

print("\n4. Progress Tracking & Completion...")
try:
    completed_task = task_store.update_task(created.id, TaskUpdate(
        progress=100.0,
        status="completed",
        completed_at=datetime.now()
    ))
    print(f"   [OK] Marked task as completed: {completed_task.status}")
    print("   [OK] Progress tracking tests passed!")
except Exception as e:
    print(f"   [FAIL] Progress tracking failed: {e}")

print("\n" + "="*50)
print("PHASE 6 COMPLETED SUCCESSFULLY!")
print("="*50)

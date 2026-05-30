
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/api/v1"

def create_task(title, subject, priority, due_date, estimated_hours, status="pending"):
    url = f"{BASE_URL}/tasks"
    payload = {
        "title": title,
        "subject": subject,
        "priority": priority,
        "due_date": due_date,
        "estimated_hours": estimated_hours,
        "status": status
    }
    response = requests.post(url, json=payload)
    result = response.json()
    if response.status_code != 200:
        print(f"Error creating task {title}: {response.text}")
    return result

def update_task(task_id, status):
    url = f"{BASE_URL}/tasks/{task_id}"
    payload = {
        "status": status
    }
    response = requests.patch(url, json=payload)
    return response.json()

def get_tasks():
    url = f"{BASE_URL}/tasks"
    response = requests.get(url)
    result = response.json()
    if response.status_code != 200:
        print(f"Error getting tasks: {response.text}")
    return result.get("data", [])

# Step 1: Create 10 tasks
print("="*80)
print("Phase 5 Validation: Task System Validation")
print("="*80)

tasks_to_create = [
    ("Complete Modern History", "History", "high", "2026-06-01", 2.0),
    ("Polity - Fundamental Rights", "Polity", "high", "2026-06-02", 1.5),
    ("Geography - Indian Climate", "Geography", "medium", "2026-06-03", 1.0),
    ("Economy - Budget", "Economics", "medium", "2026-06-04", 1.5),
    ("Environment - Biodiversity", "Environment", "low", "2026-06-05", 1.0),
    ("Science & Tech - Biotechnology", "Science & Technology", "high", "2026-06-06", 2.5),
    ("Karnataka GK - History", "Karnataka GK", "medium", "2026-06-07", 1.0),
    ("Current Affairs - May 2026", "Current Affairs", "high", "2026-06-08", 2.0),
    ("CSAT - Logical Reasoning", "CSAT", "medium", "2026-06-09", 1.5),
    ("Polity - Constitution", "Polity", "low", "2026-06-10", 1.0)
]

created_tasks = []

print("\nCreating 10 tasks...")
for title, subject, priority, due_date, estimated_hours in tasks_to_create:
    task = create_task(title, subject, priority, due_date, estimated_hours)
    created_tasks.append(task)
    print(f"Created: {title} (ID: {task.get('id', 'unknown')})")

print("\n" + "="*80)
print("Marking 5 tasks as completed...")
for i in range(5):
    task = created_tasks[i]
    task_id = task.get("id")
    if task_id:
        update_task(task_id, "completed")
        print(f"Marked as completed: {task['title']}")

print("\n" + "="*80)
print("Getting all tasks...")
tasks = get_tasks()
print(f"Total tasks: {len(tasks)}")
pending_count = 0
completed_count = 0
for t in tasks:
    if t.get("status") == "completed":
        completed_count += 1
    else:
        pending_count += 1
print(f"Completed: {completed_count}")
print(f"Pending: {pending_count}")
print(f"Completion Rate: {int((completed_count / len(tasks)) * 100)}%")

print("\n" + "="*80)
print("[Task System Validation Complete!")
print("="*80)


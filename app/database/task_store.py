
from datetime import datetime
from typing import List, Optional, Dict
import uuid
from app.schemas.tasks import Task, TaskCreate, TaskUpdate


class TaskStore:
    def __init__(self):
        self._tasks: Dict[str, Task] = {}

    def create_task(self, task_create: TaskCreate) -> Task:
        task_id = str(uuid.uuid4())
        now = datetime.now()
        task = Task(
            id=task_id,
            **task_create.model_dump(),
            status="pending",
            progress=0.0,
            created_at=now,
            updated_at=now
        )
        self._tasks[task_id] = task
        return task

    def get_task(self, task_id: str) -> Optional[Task]:
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> List[Task]:
        return list(self._tasks.values())

    def update_task(self, task_id: str, task_update: TaskUpdate) -> Optional[Task]:
        if task_id not in self._tasks:
            return None
        existing_task = self._tasks[task_id]
        update_data = task_update.model_dump(exclude_unset=True)
        updated_task = existing_task.model_copy(
            update={**update_data, "updated_at": datetime.now()}
        )
        self._tasks[task_id] = updated_task
        return updated_task

    def delete_task(self, task_id: str) -> bool:
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False


task_store = TaskStore()

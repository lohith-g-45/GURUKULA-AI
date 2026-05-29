
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
from pathlib import Path
from app.utils.logger import logger


class SharedContextStore:
    def __init__(self, storage_path: Optional[Path] = None):
        self.context: Dict[str, Any] = {}
        self.logs: List[Dict[str, Any]] = []
        self.storage_path = storage_path or Path(__file__).parent.parent.parent / "datasets" / "KAS" / "context_store.json"
        self._load_from_storage()

    def _load_from_storage(self):
        try:
            if self.storage_path.exists():
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.context = data.get("context", {})
                    self.logs = data.get("logs", [])
        except Exception as e:
            logger.error(f"Failed to load context store: {e}")

    def _save_to_storage(self):
        try:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump({
                    "context": self.context,
                    "logs": self.logs,
                    "last_updated": datetime.now().isoformat()
                }, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save context store: {e}")

    def set(self, key: str, value: Any):
        self.context[key] = value
        self._add_log("set", key, value)
        self._save_to_storage()

    def get(self, key: str, default: Any = None) -> Any:
        return self.context.get(key, default)

    def update(self, updates: Dict[str, Any]):
        self.context.update(updates)
        for key, value in updates.items():
            self._add_log("update", key, value)
        self._save_to_storage()

    def delete(self, key: str):
        if key in self.context:
            del self.context[key]
            self._add_log("delete", key, None)
            self._save_to_storage()

    def get_all(self) -> Dict[str, Any]:
        return self.context.copy()

    def _add_log(self, action: str, key: str, value: Any):
        self.logs.append({
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "key": key,
            "value": value
        })

    def get_logs(self, limit: int = 100) -> List[Dict[str, Any]]:
        return self.logs[-limit:]

    def clear(self):
        self.context = {}
        self.logs = []
        self._save_to_storage()


context_store = SharedContextStore()


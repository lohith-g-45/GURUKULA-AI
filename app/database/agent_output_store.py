
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from pathlib import Path
import json
import hashlib
from app.utils.logger import logger


class AgentOutputCache:
    def __init__(self, storage_path: Optional[Path] = None, default_ttl_hours: int = 24):
        self.storage_path = storage_path or Path(__file__).parent.parent.parent / "datasets" / "KAS" / "agent_outputs.json"
        self.default_ttl = timedelta(hours=default_ttl_hours)
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._load_from_storage()

    def _get_cache_key(self, agent_type: str, context_hash: Optional[str] = None) -> str:
        if context_hash:
            return f"{agent_type}:{context_hash}"
        return agent_type

    def _load_from_storage(self):
        try:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            if self.storage_path.exists():
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._cache = data.get('cache', {})
        except Exception as e:
            logger.error(f"Failed to load agent cache: {e}")

    def _save_to_storage(self):
        try:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'last_updated': datetime.now().isoformat(),
                    'cache': self._cache
                }, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save agent cache: {e}")

    def _hash_context(self, context: Any) -> str:
        context_str = json.dumps(context, sort_keys=True)
        return hashlib.md5(context_str.encode()).hexdigest()

    def get(self, agent_type: str, context: Optional[Any] = None) -> Optional[Dict[str, Any]]:
        context_hash = self._hash_context(context) if context else None
        key = self._get_cache_key(agent_type, context_hash)
        
        if key not in self._cache:
            return None
        
        entry = self._cache[key]
        expires_at = datetime.fromisoformat(entry['expires_at'])
        
        if datetime.now() > expires_at:
            del self._cache[key]
            self._save_to_storage()
            return None
        
        return entry['data']

    def set(
        self, 
        agent_type: str, 
        data: Dict[str, Any], 
        context: Optional[Any] = None, 
        ttl_hours: Optional[int] = None
    ):
        ttl = timedelta(hours=ttl_hours) if ttl_hours else self.default_ttl
        context_hash = self._hash_context(context) if context else None
        key = self._get_cache_key(agent_type, context_hash)
        
        self._cache[key] = {
            'data': data,
            'created_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + ttl).isoformat()
        }
        self._save_to_storage()

    def invalidate(self, agent_type: str, context: Optional[Any] = None):
        context_hash = self._hash_context(context) if context else None
        key = self._get_cache_key(agent_type, context_hash)
        
        if key in self._cache:
            del self._cache[key]
            self._save_to_storage()
            logger.info(f"Invalidated cache for {key}")

    def invalidate_all(self):
        self._cache = {}
        self._save_to_storage()
        logger.info("Invalidated all agent cache")

    def get_stats(self) -> Dict[str, Any]:
        active_entries = 0
        for entry in self._cache.values():
            expires_at = datetime.fromisoformat(entry['expires_at'])
            if datetime.now() <= expires_at:
                active_entries += 1
        
        return {
            'total_entries': len(self._cache),
            'active_entries': active_entries,
            'agent_types': list(set(k.split(':')[0] for k in self._cache.keys()))
        }


agent_output_cache = AgentOutputCache()

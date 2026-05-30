
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path
import json
from app.utils.logger import logger


class UserProfileStore:
    def __init__(self, storage_path: Optional[Path] = None):
        self.storage_path = storage_path or Path(__file__).parent.parent.parent / "datasets" / "KAS" / "user_profile.json"
        self.profile: Dict[str, Any] = {}
        self._load_from_storage()

    def _load_from_storage(self):
        try:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            if self.storage_path.exists():
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    self.profile = json.load(f)
        except Exception as e:
            logger.error(f"Failed to load user profile: {e}")

    def _save_to_storage(self):
        try:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(self.profile, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save user profile: {e}")

    def get_profile(self) -> Dict[str, Any]:
        return self.profile.copy()

    def update_profile(self, updates: Dict[str, Any]) -> Dict[str, Any]:
        self.profile.update(updates)
        self.profile['last_updated'] = datetime.now().isoformat()
        self._save_to_storage()
        return self.get_profile()

    def get_readiness_score(self) -> float:
        return self.profile.get('readiness_score', 70.0)

    def get_weak_subjects(self) -> List[str]:
        return self.profile.get('weak_subjects', [])

    def get_available_hours(self) -> float:
        return self.profile.get('available_hours_per_day', 6.0)

    def get_exam(self) -> str:
        return self.profile.get('exam', 'KAS')


class MockScoreStore:
    def __init__(self, storage_path: Optional[Path] = None):
        self.storage_path = storage_path or Path(__file__).parent.parent.parent / "datasets" / "KAS" / "mock_scores.json"
        self.scores: List[Dict[str, Any]] = []
        self._load_from_storage()

    def _load_from_storage(self):
        try:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            if self.storage_path.exists():
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    self.scores = json.load(f)
        except Exception as e:
            logger.error(f"Failed to load mock scores: {e}")

    def _save_to_storage(self):
        try:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(self.scores, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save mock scores: {e}")

    def add_mock_score(self, score_data: Dict[str, Any]) -> Dict[str, Any]:
        score_entry = {
            "id": f"mock_{len(self.scores)}",
            **score_data,
            "taken_at": datetime.now().isoformat()
        }
        self.scores.append(score_entry)
        self._save_to_storage()
        return score_entry

    def get_all_scores(self) -> List[Dict[str, Any]]:
        return self.scores.copy()

    def get_latest_score(self) -> Optional[Dict[str, Any]]:
        if not self.scores:
            return None
        return self.scores[-1].copy()


class StudySessionStore:
    def __init__(self, storage_path: Optional[Path] = None):
        self.storage_path = storage_path or Path(__file__).parent.parent.parent / "datasets" / "KAS" / "study_sessions.json"
        self.sessions: List[Dict[str, Any]] = []
        self._load_from_storage()

    def _load_from_storage(self):
        try:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            if self.storage_path.exists():
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    self.sessions = json.load(f)
        except Exception as e:
            logger.error(f"Failed to load study sessions: {e}")

    def _save_to_storage(self):
        try:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(self.sessions, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save study sessions: {e}")

    def add_session(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        session_entry = {
            "id": f"session_{len(self.sessions)}",
            **session_data,
            "started_at": datetime.now().isoformat()
        }
        self.sessions.append(session_entry)
        self._save_to_storage()
        return session_entry

    def get_sessions_today(self) -> List[Dict[str, Any]]:
        today = datetime.now().date().isoformat()
        return [
            s for s in self.sessions if s.get('started_at', '').startswith(today)
        ]

    def get_total_hours_today(self) -> float:
        sessions = self.get_sessions_today()
        total_hours = 0.0
        for session in sessions:
            if 'duration_hours' in session:
                total_hours += session['duration_hours']
        return total_hours

    def get_study_streak(self) -> int:
        if not self.sessions:
            return 0
        dates = [datetime.fromisoformat(s['started_at']).date() for s in self.sessions]
        unique_dates = list(sorted(list(set(dates)), reverse=True))
        streak = 0
        current = datetime.now().date()
        for date in unique_dates:
            delta = (current - date).days
            if delta > 1:
                break
            streak += 1
            current = date
        return streak


user_profile_store = UserProfileStore()
mock_score_store = MockScoreStore()
study_session_store = StudySessionStore()


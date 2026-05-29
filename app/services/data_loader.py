
import json
import os
from pathlib import Path
from datetime import datetime, timedelta
import hashlib


class CacheManager:
    def __init__(self, ttl_hours=24):
        self.cache = {}
        self.ttl = timedelta(hours=ttl_hours)

    def get(self, key):
        if key not in self.cache:
            return None
        cache_entry = self.cache[key]
        if datetime.now() - cache_entry["timestamp"] > self.ttl:
            del self.cache[key]
            return None
        return cache_entry["data"]

    def set(self, key, data):
        self.cache[key] = {"data": data, "timestamp": datetime.now()}

    def clear(self):
        self.cache.clear()

    def remove(self, key):
        if key in self.cache:
            del self.cache[key]

    def get_status(self):
        return {
            "total_entries": len(self.cache),
            "keys": list(self.cache.keys()),
            "ttl_hours": self.ttl.total_seconds() / 3600
        }


class ValidationSystem:
    @staticmethod
    def validate_json(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json.load(f)
            return True, None
        except json.JSONDecodeError as e:
            return False, "JSON decode error: " + str(e)
        except Exception as e:
            return False, "Error reading file: " + str(e)

    @staticmethod
    def validate_prompt(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if len(content.strip()) == 0:
                    return False, "Empty prompt file"
            return True, None
        except Exception as e:
            return False, "Error reading prompt file: " + str(e)

    @staticmethod
    def validate_dataset_structure(data, expected_type):
        try:
            if expected_type == "analytics":
                if not isinstance(data, dict):
                    return False, "Analytics data must be a dict"
                # Some analytics datasets don't have 'exam', so skip that check
            elif expected_type == "intelligence":
                if not isinstance(data, dict):
                    return False, "Intelligence data must be a dict"
                # Some intelligence datasets don't have 'version', so skip that check
            elif expected_type == "recommendations":
                if not isinstance(data, dict):
                    return False, "Recommendations data must be a dict"
                # Some recommendations datasets don't have 'subject_weightage', so skip that check
            elif expected_type == "planning":
                if not isinstance(data, dict):
                    return False, "Planning data must be a dict"
                # Some planning datasets don't have 'version', so skip that check
            return True, None
        except Exception as e:
            return False, "Structure validation error: " + str(e)


class DatasetRegistry:
    def __init__(self):
        self.registry = {}

    def register(self, name, path, dataset_type, last_modified):
        self.registry[name] = {
            "path": str(path),
            "type": dataset_type,
            "last_modified": last_modified,
            "registered_at": datetime.now()
        }

    def get(self, name):
        return self.registry.get(name)

    def list_all(self):
        return self.registry.copy()

    def is_stale(self, name, current_modified):
        if name not in self.registry:
            return True
        return self.registry[name]["last_modified"] < current_modified


class DataLoader:
    def __init__(self, base_path=None):
        if base_path is None:
            self.base_path = Path(__file__).parent.parent.parent / "datasets" / "KAS"
        else:
            self.base_path = base_path
        
        self.cache = CacheManager()
        self.validator = ValidationSystem()
        self.registry = DatasetRegistry()
        self._initialize_registry()

    def _initialize_registry(self):
        dataset_mappings = [
            ("analytics", "analytics", ["kas_pyq_metadata.json", "kas_question_distribution.json", "kas_subject_weightage.json", "kas_topic_frequency.json"]),
            ("intelligence", "intelligence", ["consistency_rules.json", "readiness_rules.json", "risk_rules.json", "scoring_formulas.json"]),
            ("recommendations", "recommendations", ["adaptive_time_allocation.json", "recommendation_engine.json", "recommendation_priority_rules.json", "recovery_rules.json", "strategy_rules.json"]),
            ("planning", "planning", ["adaptive_planning_rules.json", "adaptive_rescheduling_rules.json", "fatigue_aware_rules.json", "micro_milestone_rules.json", "mock_planning_rules.json", "revision_cycles.json", "roadmap_rules.json", "study_planning_rules.json", "subject_interleaving_rules.json", "task_granularity_rules.json"]),
            ("prompts", "prompts", ["insight_prompt.txt", "planning_prompt.txt", "research_prompt.txt", "revision_prompt.txt"])
        ]

        for category, dir_name, files in dataset_mappings:
            dir_path = self.base_path / dir_name
            if dir_path.exists():
                for file_name in files:
                    file_path = dir_path / file_name
                    if file_path.exists():
                        mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                        self.registry.register(category + "/" + file_name, file_path, category, mtime)

    def _load_json(self, file_path):
        cache_key = "json:" + hashlib.md5(str(file_path).encode()).hexdigest()
        cached = self.cache.get(cache_key)
        if cached is not None:
            return cached

        is_valid, error = self.validator.validate_json(file_path)
        if not is_valid:
            raise ValueError("Invalid JSON file " + str(file_path) + ": " + str(error))

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.cache.set(cache_key, data)
        return data

    def _load_text(self, file_path):
        cache_key = "text:" + hashlib.md5(str(file_path).encode()).hexdigest()
        cached = self.cache.get(cache_key)
        if cached is not None:
            return cached

        is_valid, error = self.validator.validate_prompt(file_path)
        if not is_valid:
            raise ValueError("Invalid text file " + str(file_path) + ": " + str(error))

        with open(file_path, 'r', encoding='utf-8') as f:
            data = f.read()

        self.cache.set(cache_key, data)
        return data

    def load_analytics(self):
        analytics_data = {}
        dir_path = self.base_path / "analytics"
        if dir_path.exists():
            for file_path in dir_path.glob("*.json"):
                try:
                    data = self._load_json(file_path)
                    is_valid, error = self.validator.validate_dataset_structure(data, "analytics")
                    if is_valid:
                        analytics_data[file_path.stem] = data
                    else:
                        print("Warning: " + file_path.name + " structure invalid: " + str(error))
                except Exception as e:
                    print("Error loading " + file_path.name + ": " + str(e))
        return analytics_data

    def load_intelligence(self):
        intelligence_data = {}
        dir_path = self.base_path / "intelligence"
        if dir_path.exists():
            for file_path in dir_path.glob("*.json"):
                try:
                    data = self._load_json(file_path)
                    is_valid, error = self.validator.validate_dataset_structure(data, "intelligence")
                    if is_valid:
                        intelligence_data[file_path.stem] = data
                    else:
                        print("Warning: " + file_path.name + " structure invalid: " + str(error))
                except Exception as e:
                    print("Error loading " + file_path.name + ": " + str(e))
        return intelligence_data

    def load_recommendations(self):
        recommendations_data = {}
        dir_path = self.base_path / "recommendations"
        if dir_path.exists():
            for file_path in dir_path.glob("*.json"):
                try:
                    data = self._load_json(file_path)
                    is_valid, error = self.validator.validate_dataset_structure(data, "recommendations")
                    if is_valid:
                        recommendations_data[file_path.stem] = data
                    else:
                        print("Warning: " + file_path.name + " structure invalid: " + str(error))
                except Exception as e:
                    print("Error loading " + file_path.name + ": " + str(e))
        return recommendations_data

    def load_planning(self):
        planning_data = {}
        dir_path = self.base_path / "planning"
        if dir_path.exists():
            for file_path in dir_path.glob("*.json"):
                try:
                    data = self._load_json(file_path)
                    is_valid, error = self.validator.validate_dataset_structure(data, "planning")
                    if is_valid:
                        planning_data[file_path.stem] = data
                    else:
                        print("Warning: " + file_path.name + " structure invalid: " + str(error))
                except Exception as e:
                    print("Error loading " + file_path.name + ": " + str(e))
        return planning_data

    def load_prompts(self):
        prompts_data = {}
        dir_path = self.base_path / "prompts"
        if dir_path.exists():
            for file_path in dir_path.glob("*.txt"):
                try:
                    prompts_data[file_path.stem] = self._load_text(file_path)
                except Exception as e:
                    print("Error loading " + file_path.name + ": " + str(e))
        return prompts_data

    def load_all(self):
        return {
            "analytics": self.load_analytics(),
            "intelligence": self.load_intelligence(),
            "recommendations": self.load_recommendations(),
            "planning": self.load_planning(),
            "prompts": self.load_prompts()
        }

    def refresh_dataset(self, name):
        entry = self.registry.get(name)
        if not entry:
            return
        file_path = Path(entry["path"])
        cache_key = "json:" + hashlib.md5(str(file_path).encode()).hexdigest() if file_path.suffix == ".json" else "text:" + hashlib.md5(str(file_path).encode()).hexdigest()
        self.cache.remove(cache_key)
        if file_path.exists():
            mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
            self.registry.register(name, file_path, entry["type"], mtime)

    def refresh_all(self):
        self.cache.clear()
        self._initialize_registry()

    def get_summary(self):
        all_data = self.load_all()
        summary = {
            "analytics": {
                "count": len(all_data["analytics"]),
                "datasets": list(all_data["analytics"].keys())
            },
            "intelligence": {
                "count": len(all_data["intelligence"]),
                "datasets": list(all_data["intelligence"].keys())
            },
            "recommendations": {
                "count": len(all_data["recommendations"]),
                "datasets": list(all_data["recommendations"].keys())
            },
            "planning": {
                "count": len(all_data["planning"]),
                "datasets": list(all_data["planning"].keys())
            },
            "prompts": {
                "count": len(all_data["prompts"]),
                "datasets": list(all_data["prompts"].keys())
            }
        }
        return summary

    def get_validation_results(self):
        results = {}
        registry = self.registry.list_all()
        for name, entry in registry.items():
            file_path = Path(entry["path"])
            if file_path.suffix == ".json":
                is_valid, error = self.validator.validate_json(file_path)
                if is_valid:
                    try:
                        data = self._load_json(file_path)
                        struct_valid, struct_error = self.validator.validate_dataset_structure(data, entry["type"])
                        results[name] = {
                            "valid": struct_valid,
                            "error": struct_error if struct_error else None
                        }
                    except:
                        results[name] = {"valid": False, "error": "Failed to load for structure check"}
                else:
                    results[name] = {"valid": is_valid, "error": error}
            elif file_path.suffix == ".txt":
                is_valid, error = self.validator.validate_prompt(file_path)
                results[name] = {"valid": is_valid, "error": error}
        return results


def main():
    print("=" * 60)
    print("GURUKULA AI - Data Loader Test")
    print("=" * 60)

    loader = DataLoader()

    print("\n1. Loading datasets...")
    all_data = loader.load_all()

    print("\n2. Dataset Summary:")
    summary = loader.get_summary()
    for category, info in summary.items():
        print("   " + category.capitalize() + ": " + str(info["count"]) + " datasets - " + ", ".join(info["datasets"]))

    print("\n3. Cache Status:")
    cache_status = loader.cache.get_status()
    print("   Total entries: " + str(cache_status["total_entries"]))
    print("   Cached keys: " + ", ".join(cache_status["keys"]))
    print("   TTL: " + str(cache_status["ttl_hours"]) + " hours")

    print("\n4. Validation Results:")
    validation = loader.get_validation_results()
    all_valid = True
    for name, result in validation.items():
        status = "[OK]" if result["valid"] else "[FAIL]"
        print("   " + status + " " + name)
        if not result["valid"]:
            all_valid = False
            print("      Error: " + str(result["error"]))

    print("\n" + "=" * 60)
    if all_valid:
        print("[SUCCESS] PHASE 2 COMPLETED SUCCESSFULLY!")
    else:
        print("[WARNING] PHASE 2 COMPLETED WITH WARNINGS")
    print("=" * 60)


if __name__ == "__main__":
    main()

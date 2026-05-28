import os
from utils.json_utils import save_json, load_json
from utils.dataset_manager import get_data_path


def generate_subject_priority(exam_name, syllabus_data):
    subjects = syllabus_data.get("subjects", [])
    priority_scores = []
    
    for subject in subjects:
        weightage = subject.get("estimated_weightage", 10)
        difficulty_score = {"Easy": 1, "Easy-Medium": 2, "Medium": 3, "Hard": 4}.get(
            subject.get("difficulty", "Medium"), 3
        )
        priority_score = weightage * (5 - difficulty_score)
        
        priority_scores.append({
            "subject": subject.get("name"),
            "priority_score": priority_score,
            "estimated_weightage": weightage,
            "difficulty": subject.get("difficulty"),
            "preparation_complexity": subject.get("preparation_complexity", "Medium"),
            "revision_frequency": subject.get("revision_frequency", "Weekly"),
            "recommended_revision_gap": subject.get("recommended_revision_gap", "3-5 days"),
            "weak_area_focus": subject.get("weak_area_focus", "High")
        })
    
    priority_scores.sort(key=lambda x: x["priority_score"], reverse=True)
    return priority_scores


def generate_revision_priority(exam_name, syllabus_data):
    revision_priority = []
    
    for subject in syllabus_data.get("subjects", []):
        for topic in subject.get("topics", []):
            revision_priority.append({
                "subject": subject.get("name"),
                "topic": topic.get("name"),
                "importance": topic.get("importance", "Medium"),
                "pyq_frequency": topic.get("pyq_frequency", "Medium"),
                "revision_priority": topic.get("revision_priority", "Medium"),
                "estimated_prep_time": topic.get("estimated_prep_time", "2-3 hours"),
                "weak_topic_sensitivity": topic.get("weak_topic_sensitivity", "Medium")
            })
    
    priority_order = {"Very High": 4, "High": 3, "Medium": 2, "Low": 1}
    revision_priority.sort(
        key=lambda x: (
            priority_order.get(x["importance"], 2), 
            priority_order.get(x["pyq_frequency"], 2)
        ), 
        reverse=True
    )
    
    return revision_priority


def generate_topic_frequency(exam_name, syllabus_data):
    topic_frequency = []
    
    for subject in syllabus_data.get("subjects", []):
        for topic in subject.get("topics", []):
            freq_score = {"Very High": 10, "High": 7, "Medium": 4, "Low": 2}.get(
                topic.get("pyq_frequency", "Medium"), 4
            )
            topic_frequency.append({
                "subject": subject.get("name"),
                "topic": topic.get("name"),
                "frequency_score": freq_score,
                "importance": topic.get("importance", "Medium")
            })
    
    topic_frequency.sort(key=lambda x: x["frequency_score"], reverse=True)
    return topic_frequency


def generate_prep_difficulty(exam_name, syllabus_data):
    categories = {
        "easy_subjects": [],
        "medium_subjects": [],
        "hard_subjects": [],
        "time_consuming_subjects": []
    }
    
    for subject in syllabus_data.get("subjects", []):
        name = subject.get("name")
        difficulty = subject.get("difficulty", "Medium")
        complexity = subject.get("preparation_complexity", "Medium")
        
        if difficulty in ["Easy", "Easy-Medium"]:
            categories["easy_subjects"].append(name)
        elif difficulty == "Medium":
            categories["medium_subjects"].append(name)
        else:
            categories["hard_subjects"].append(name)
        
        if complexity in ["High", "Very High"]:
            categories["time_consuming_subjects"].append(name)
    
    return categories


def generate_readiness_rules(exam_name, syllabus_data):
    return {
        "research_agent": {
            "focus_areas": [f"{exam_name} exam pattern and syllabus", "Subject weightage and priority", "PYQ trends and frequently asked topics"],
            "data_needed": ["syllabus", "pyqs", "weightage"]
        },
        "planning_agent": {
            "focus_areas": ["Time allocation", "Subject sequencing", "Weekly study targets"],
            "data_needed": ["subject_priority", "prep_difficulty"]
        },
        "revision_agent": {
            "focus_areas": ["Weak areas", "High-frequency topics", "Revision scheduling"],
            "data_needed": ["revision_priority", "topic_frequency"]
        },
        "insight_agent": {
            "focus_areas": ["Exam patterns", "Success factors", "Preparation strategies"],
            "data_needed": ["topic_frequency", "pyq_trends"]
        }
    }


def save_analytics(analytics_data, exam_name, base_dir="datasets"):
    analytics_dir = get_data_path(exam_name, "analytics")
    os.makedirs(analytics_dir, exist_ok=True)
    
    for filename, data in analytics_data.items():
        save_path = os.path.join(analytics_dir, filename)
        save_json(data, save_path)
    
    return True

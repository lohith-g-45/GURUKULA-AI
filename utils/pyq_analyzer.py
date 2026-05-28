import re
import os
from collections import defaultdict
from utils.json_utils import save_json
from utils.pdf_downloader import extract_pdf_text


KAS_SUBJECTS = [
    "History", "Polity", "Geography", "Economics",
    "Environment", "Science", "Karnataka GK",
    "Mental Ability", "Current Affairs"
]

KAS_TOPICS = {
    "History": ["Ancient India", "Medieval India", "Modern India", "Karnataka History"],
    "Polity": ["Constitution", "Governance", "State Government", "Local Bodies"],
    "Geography": ["Indian Geography", "Karnataka Geography", "Physical Geography"],
    "Economics": ["Indian Economy", "Karnataka Economy", "Budget", "Schemes"],
    "Environment": ["Ecology", "Biodiversity", "Climate Change"],
    "Science": ["Physics", "Chemistry", "Biology", "Technology"],
    "Karnataka GK": ["History", "Culture", "Geography", "Economy"],
    "Mental Ability": ["Logical Reasoning", "Numerical Ability", "Data Interpretation"],
    "Current Affairs": ["National", "International", "Karnataka"]
}


def extract_text_from_pyq_dir(exam_name):
    pyq_dir = os.path.join("datasets", exam_name, "pyqs")
    extracted_texts = {}
    
    if not os.path.exists(pyq_dir):
        return extracted_texts
    
    for filename in os.listdir(pyq_dir):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(pyq_dir, filename)
            text = extract_pdf_text(pdf_path)
            if text:
                extracted_texts[filename] = text
                # Save raw text
                raw_dir = os.path.join("datasets", exam_name, "raw")
                os.makedirs(raw_dir, exist_ok=True)
                raw_file = os.path.join(raw_dir, f"{filename.replace('.pdf', '.txt')}")
                with open(raw_file, "w", encoding="utf-8") as f:
                    f.write(text)
    
    return extracted_texts


def count_topic_frequency(texts, subject_topics):
    frequency = defaultdict(int)
    
    for filename, text in texts.items():
        text_lower = text.lower()
        for subject, topics in subject_topics.items():
            for topic in topics:
                count = text_lower.count(topic.lower())
                if count > 0:
                    key = f"{subject} - {topic}"
                    frequency[key] += count
    
    return dict(sorted(frequency.items(), key=lambda x: x[1], reverse=True))


def calculate_subject_weightage(frequency, subject_names):
    weightage = {}
    total = sum(frequency.values()) if frequency else 0
    
    if total == 0:
        for subject in subject_names:
            weightage[subject] = {"prelims_weightage": 0, "mains_weightage": 0, "priority": "Low", "difficulty": "Medium"}
        return weightage
    
    for subject in subject_names:
        subject_total = 0
        for key, count in frequency.items():
            if key.startswith(f"{subject} -"):
                subject_total += count
        
        prelims_weightage = round((subject_total / total) * 100)
        weightage[subject] = {
            "prelims_weightage": prelims_weightage,
            "mains_weightage": prelims_weightage * 3,
            "priority": "Very High" if prelims_weightage > 15 else ("High" if prelims_weightage > 8 else "Medium"),
            "difficulty": "Medium"
        }
    
    return weightage


def generate_analytics_from_pyqs(exam_name):
    """Generate all analytics from real PYQ data"""
    extracted_texts = extract_text_from_pyq_dir(exam_name)
    topic_frequency = count_topic_frequency(extracted_texts, KAS_TOPICS)
    subject_weightage = calculate_subject_weightage(topic_frequency, KAS_SUBJECTS)
    
    # Save topic frequency
    analytics_dir = os.path.join("datasets", exam_name, "analytics")
    os.makedirs(analytics_dir, exist_ok=True)
    topic_freq_path = os.path.join(analytics_dir, "topic_frequency.json")
    save_json(topic_frequency, topic_freq_path)
    
    # Save subject weightage
    weightage_dir = os.path.join("datasets", exam_name, "weightage")
    os.makedirs(weightage_dir, exist_ok=True)
    weightage_path = os.path.join(weightage_dir, f"{exam_name}_weightage.json")
    save_json({"exam": exam_name, "subjects": subject_weightage, "total_marks": {"prelims": 200, "mains": 1000}}, weightage_path)
    
    return {"topic_frequency": topic_frequency, "subject_weightage": subject_weightage}

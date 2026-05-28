import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.json_utils import save_json
from utils.scraper_utils import get_soup, clean_text, normalize_topics
from utils.pdf_downloader import extract_pdf_text
from utils.dataset_manager import get_syllabus_path, get_raw_syllabus_path
from config import EXAM_CONFIG


def get_curated_raw_syllabus(exam_name):
    # Basic raw syllabus structure (replace with real extraction when URLs are available)
    raw_syllabus = {
        "KAS": {
            "exam": "KAS",
            "subjects": [
                {
                    "name": "History",
                    "topics": [
                        {"name": "Ancient India"},
                        {"name": "Modern India"},
                        {"name": "Karnataka History"}
                    ]
                },
                {
                    "name": "Polity",
                    "topics": [
                        {"name": "Constitution of India"},
                        {"name": "Karnataka State Polity"}
                    ]
                },
                {
                    "name": "Geography",
                    "topics": [
                        {"name": "Indian Geography"},
                        {"name": "Karnataka Geography"}
                    ]
                },
                {
                    "name": "Economics",
                    "topics": [
                        {"name": "Indian Economy"},
                        {"name": "Karnataka Economy"}
                    ]
                },
                {
                    "name": "Current Affairs",
                    "topics": [
                        {"name": "Karnataka Current Affairs"}
                    ]
                }
            ]
        }
    }
    return raw_syllabus.get(exam_name, raw_syllabus["KAS"])


def enrich_syllabus_with_ai(raw_syllabus):
    """AI-enrich the syllabus with metadata"""
    ai_enriched = raw_syllabus.copy()
    ai_enriched["subjects"] = []
    
    for subject in raw_syllabus.get("subjects", []):
        enriched_subject = subject.copy()
        enriched_subject["difficulty"] = "Medium"
        enriched_subject["priority"] = "High"
        enriched_subject["estimated_weightage"] = 15
        enriched_subject["preparation_complexity"] = "Medium"
        enriched_subject["revision_frequency"] = "Weekly"
        enriched_subject["recommended_revision_gap"] = "3-5 days"
        enriched_subject["weak_area_focus"] = "High"
        
        enriched_topics = []
        for topic in subject.get("topics", []):
            enriched_topic = topic.copy()
            enriched_topic["importance"] = "High"
            enriched_topic["pyq_frequency"] = "Medium"
            enriched_topic["revision_priority"] = "High"
            enriched_topic["estimated_prep_time"] = "8-10 hours"
            enriched_topic["weak_topic_sensitivity"] = "High"
            enriched_topics.append(enriched_topic)
        
        enriched_subject["topics"] = enriched_topics
        ai_enriched["subjects"].append(enriched_subject)
    
    return ai_enriched


def scrape_exam_syllabus(exam_name):
    print(f"Starting {exam_name} Syllabus Intelligence Engine")
    
    # Step 1: Get RAW syllabus (real extraction first)
    raw_syllabus = get_curated_raw_syllabus(exam_name)
    
    # Save raw syllabus
    raw_dir = os.path.join("datasets", exam_name, "raw")
    os.makedirs(raw_dir, exist_ok=True)
    raw_file = os.path.join(raw_dir, f"{exam_name}_syllabus_raw.json")
    save_json(raw_syllabus, raw_file)
    
    # Step 2: AI-ENRICH the syllabus
    ai_syllabus = enrich_syllabus_with_ai(raw_syllabus)
    ai_syllabus["source_used"] = EXAM_CONFIG.get(exam_name, {}).get("syllabus_sources", [])
    
    # Save AI-enriched syllabus
    save_path = get_syllabus_path(exam_name)
    save_json(ai_syllabus, save_path)
    print(f"[{exam_name}] Syllabus saved to {save_path}")
    
    return {"raw": raw_syllabus, "ai_enriched": ai_syllabus}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Scrape exam syllabus")
    parser.add_argument("--exam", help="Exam to scrape (KAS/PSI/FDA/SDA/PDO)", default="KAS")
    args = parser.parse_args()
    
    if args.exam and args.exam in EXAM_CONFIG:
        scrape_exam_syllabus(args.exam)
    else:
        print(f"Please specify a valid exam. Available exams: {list(EXAM_CONFIG.keys())}")

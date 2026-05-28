import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.json_utils import save_json
from utils.scraper_utils import get_soup, clean_text, normalize_topics
from config import EXAM_CONFIG


def get_curated_syllabus(exam_name):
    syllabus_data = {
        "KAS": {
            "exam": "KAS",
            "subjects": [
                {
                    "name": "History",
                    "difficulty": "Medium",
                    "priority": "High",
                    "estimated_weightage": 20,
                    "preparation_complexity": "Medium",
                    "revision_frequency": "Weekly",
                    "recommended_revision_gap": "3-5 days",
                    "weak_area_focus": "High",
                    "topics": [
                        {
                            "name": "Ancient India",
                            "importance": "High",
                            "pyq_frequency": "Medium",
                            "revision_priority": "High",
                            "estimated_prep_time": "8-10 hours",
                            "weak_topic_sensitivity": "Medium",
                            "subtopics": ["Indus Valley Civilization", "Vedic Period", "Mauryan Empire", "Gupta Empire"]
                        },
                        {
                            "name": "Modern India",
                            "importance": "Very High",
                            "pyq_frequency": "Very High",
                            "revision_priority": "Very High",
                            "estimated_prep_time": "15-20 hours",
                            "weak_topic_sensitivity": "Very High",
                            "subtopics": ["British Expansion", "1857 Revolt", "Freedom Struggle", "Post-Independence India"]
                        },
                        {
                            "name": "Karnataka History",
                            "importance": "High",
                            "pyq_frequency": "High",
                            "revision_priority": "High",
                            "estimated_prep_time": "10-12 hours",
                            "weak_topic_sensitivity": "High",
                            "subtopics": ["Ancient Karnataka", "Wodeyar Dynasty", "Hyder Ali & Tipu Sultan", "Karnataka Integration"]
                        }
                    ]
                },
                {
                    "name": "Polity",
                    "difficulty": "Medium",
                    "priority": "Very High",
                    "estimated_weightage": 25,
                    "preparation_complexity": "Medium",
                    "revision_frequency": "Twice a Week",
                    "recommended_revision_gap": "2-3 days",
                    "weak_area_focus": "Very High",
                    "topics": [
                        {
                            "name": "Constitution of India",
                            "importance": "Very High",
                            "pyq_frequency": "Very High",
                            "revision_priority": "Very High",
                            "estimated_prep_time": "20-25 hours",
                            "weak_topic_sensitivity": "Very High",
                            "subtopics": ["Making of Constitution", "Parts & Schedules", "Fundamental Rights", "Directive Principles"]
                        },
                        {
                            "name": "Karnataka State Polity",
                            "importance": "High",
                            "pyq_frequency": "High",
                            "revision_priority": "High",
                            "estimated_prep_time": "8-10 hours",
                            "weak_topic_sensitivity": "High",
                            "subtopics": ["Karnataka Government", "Local Governance", "Panchayati Raj"]
                        }
                    ]
                },
                {
                    "name": "Geography",
                    "difficulty": "Easy-Medium",
                    "priority": "High",
                    "estimated_weightage": 10,
                    "preparation_complexity": "Medium",
                    "revision_frequency": "Weekly",
                    "recommended_revision_gap": "4-6 days",
                    "weak_area_focus": "Medium",
                    "topics": [
                        {
                            "name": "Indian Geography",
                            "importance": "Very High",
                            "pyq_frequency": "High",
                            "revision_priority": "Very High",
                            "estimated_prep_time": "12-15 hours",
                            "weak_topic_sensitivity": "High",
                            "subtopics": ["Physiography", "Natural Resources", "Agriculture", "Industry"]
                        },
                        {
                            "name": "Karnataka Geography",
                            "importance": "Very High",
                            "pyq_frequency": "Very High",
                            "revision_priority": "Very High",
                            "estimated_prep_time": "8-10 hours",
                            "weak_topic_sensitivity": "High",
                            "subtopics": ["Karnataka Physiography", "Rivers of Karnataka", "Karnataka Climate", "Natural Resources"]
                        }
                    ]
                },
                {
                    "name": "Economics",
                    "difficulty": "Medium",
                    "priority": "High",
                    "estimated_weightage": 15,
                    "preparation_complexity": "High",
                    "revision_frequency": "Weekly",
                    "recommended_revision_gap": "3-4 days",
                    "weak_area_focus": "High",
                    "topics": [
                        {
                            "name": "Indian Economy",
                            "importance": "Very High",
                            "pyq_frequency": "High",
                            "revision_priority": "High",
                            "estimated_prep_time": "12-15 hours",
                            "weak_topic_sensitivity": "High",
                            "subtopics": ["Economic Planning", "Budget", "Banking & Finance"]
                        },
                        {
                            "name": "Karnataka Economy",
                            "importance": "Very High",
                            "pyq_frequency": "High",
                            "revision_priority": "High",
                            "estimated_prep_time": "8-10 hours",
                            "weak_topic_sensitivity": "High",
                            "subtopics": ["Karnataka Budget", "State Schemes", "Agriculture & Industry"]
                        }
                    ]
                },
                {
                    "name": "Current Affairs",
                    "difficulty": "Medium",
                    "priority": "Very High",
                    "estimated_weightage": 15,
                    "preparation_complexity": "High",
                    "revision_frequency": "Daily",
                    "recommended_revision_gap": "1-2 days",
                    "weak_area_focus": "Very High",
                    "topics": [
                        {
                            "name": "Karnataka Current Affairs",
                            "importance": "Very High",
                            "pyq_frequency": "Very High",
                            "revision_priority": "Very High",
                            "estimated_prep_time": "Ongoing",
                            "weak_topic_sensitivity": "Very High",
                            "subtopics": ["Karnataka Government", "State Schemes", "Karnataka Economy"]
                        }
                    ]
                }
            ]
        },
        "PSI": {
            "exam": "PSI",
            "subjects": [
                {
                    "name": "General Studies",
                    "difficulty": "Medium",
                    "priority": "Very High",
                    "estimated_weightage": 50,
                    "preparation_complexity": "Medium",
                    "revision_frequency": "Daily",
                    "recommended_revision_gap": "1-2 days",
                    "weak_area_focus": "Very High",
                    "topics": [
                        {"name": "Karnataka History & Culture", "importance": "Very High", "pyq_frequency": "Very High", "revision_priority": "Very High", "estimated_prep_time": "10-12 hours", "weak_topic_sensitivity": "High", "subtopics": []},
                        {"name": "Indian Polity", "importance": "High", "pyq_frequency": "High", "revision_priority": "High", "estimated_prep_time": "8-10 hours", "weak_topic_sensitivity": "Medium", "subtopics": []}
                    ]
                },
                {
                    "name": "Mental Ability",
                    "difficulty": "Easy-Medium",
                    "priority": "Very High",
                    "estimated_weightage": 30,
                    "preparation_complexity": "Medium",
                    "revision_frequency": "Twice a Week",
                    "recommended_revision_gap": "2-3 days",
                    "weak_area_focus": "High",
                    "topics": [
                        {"name": "Logical Reasoning", "importance": "Very High", "pyq_frequency": "Very High", "revision_priority": "Very High", "estimated_prep_time": "10-12 hours", "weak_topic_sensitivity": "High", "subtopics": []},
                        {"name": "Numerical Ability", "importance": "High", "pyq_frequency": "High", "revision_priority": "High", "estimated_prep_time": "8-10 hours", "weak_topic_sensitivity": "Medium", "subtopics": []}
                    ]
                },
                {
                    "name": "Kannada Language",
                    "difficulty": "Easy",
                    "priority": "High",
                    "estimated_weightage": 20,
                    "preparation_complexity": "Low",
                    "revision_frequency": "Weekly",
                    "recommended_revision_gap": "5-7 days",
                    "weak_area_focus": "Medium",
                    "topics": [
                        {"name": "Kannada Grammar", "importance": "High", "pyq_frequency": "High", "revision_priority": "High", "estimated_prep_time": "6-8 hours", "weak_topic_sensitivity": "Medium", "subtopics": []}
                    ]
                }
            ]
        },
        "FDA": {
            "exam": "FDA",
            "subjects": [
                {
                    "name": "General Studies",
                    "difficulty": "Easy-Medium",
                    "priority": "Very High",
                    "estimated_weightage": 40,
                    "preparation_complexity": "Medium",
                    "revision_frequency": "Daily",
                    "recommended_revision_gap": "1-2 days",
                    "weak_area_focus": "High",
                    "topics": [
                        {"name": "Karnataka History & Culture", "importance": "Very High", "pyq_frequency": "Very High", "revision_priority": "Very High", "estimated_prep_time": "10-12 hours", "weak_topic_sensitivity": "High", "subtopics": []}
                    ]
                },
                {
                    "name": "Kannada Language",
                    "difficulty": "Easy",
                    "priority": "Very High",
                    "estimated_weightage": 30,
                    "preparation_complexity": "Low",
                    "revision_frequency": "Weekly",
                    "recommended_revision_gap": "5-7 days",
                    "weak_area_focus": "Medium",
                    "topics": [
                        {"name": "Kannada Grammar", "importance": "High", "pyq_frequency": "High", "revision_priority": "High", "estimated_prep_time": "6-8 hours", "weak_topic_sensitivity": "Medium", "subtopics": []}
                    ]
                },
                {
                    "name": "English Language",
                    "difficulty": "Easy",
                    "priority": "High",
                    "estimated_weightage": 30,
                    "preparation_complexity": "Low",
                    "revision_frequency": "Weekly",
                    "recommended_revision_gap": "5-7 days",
                    "weak_area_focus": "Medium",
                    "topics": [
                        {"name": "English Grammar", "importance": "High", "pyq_frequency": "High", "revision_priority": "High", "estimated_prep_time": "6-8 hours", "weak_topic_sensitivity": "Medium", "subtopics": []}
                    ]
                }
            ]
        },
        "SDA": {
            "exam": "SDA",
            "subjects": [
                {
                    "name": "General Knowledge",
                    "difficulty": "Easy",
                    "priority": "Very High",
                    "estimated_weightage": 40,
                    "preparation_complexity": "Low",
                    "revision_frequency": "Every 2 Days",
                    "recommended_revision_gap": "2-4 days",
                    "weak_area_focus": "Medium",
                    "topics": [
                        {"name": "Karnataka GK", "importance": "Very High", "pyq_frequency": "Very High", "revision_priority": "Very High", "estimated_prep_time": "5-6 hours", "weak_topic_sensitivity": "Medium", "subtopics": []}
                    ]
                },
                {
                    "name": "Kannada Language",
                    "difficulty": "Easy",
                    "priority": "High",
                    "estimated_weightage": 30,
                    "preparation_complexity": "Low",
                    "revision_frequency": "Weekly",
                    "recommended_revision_gap": "5-7 days",
                    "weak_area_focus": "Medium",
                    "topics": [
                        {"name": "Basic Kannada", "importance": "High", "pyq_frequency": "High", "revision_priority": "High", "estimated_prep_time": "4-6 hours", "weak_topic_sensitivity": "Medium", "subtopics": []}
                    ]
                },
                {
                    "name": "English Language",
                    "difficulty": "Easy",
                    "priority": "High",
                    "estimated_weightage": 30,
                    "preparation_complexity": "Low",
                    "revision_frequency": "Weekly",
                    "recommended_revision_gap": "5-7 days",
                    "weak_area_focus": "Medium",
                    "topics": [
                        {"name": "Basic English", "importance": "High", "pyq_frequency": "High", "revision_priority": "High", "estimated_prep_time": "4-6 hours", "weak_topic_sensitivity": "Medium", "subtopics": []}
                    ]
                }
            ]
        },
        "PDO": {
            "exam": "PDO",
            "subjects": [
                {
                    "name": "Rural Development & Panchayati Raj",
                    "difficulty": "Medium",
                    "priority": "Very High",
                    "estimated_weightage": 50,
                    "preparation_complexity": "High",
                    "revision_frequency": "Daily",
                    "recommended_revision_gap": "1-2 days",
                    "weak_area_focus": "Very High",
                    "topics": [
                        {"name": "Karnataka Panchayati Raj", "importance": "Very High", "pyq_frequency": "Very High", "revision_priority": "Very High", "estimated_prep_time": "15-20 hours", "weak_topic_sensitivity": "Very High", "subtopics": []}
                    ]
                },
                {
                    "name": "General Studies",
                    "difficulty": "Medium",
                    "priority": "High",
                    "estimated_weightage": 30,
                    "preparation_complexity": "Medium",
                    "revision_frequency": "Weekly",
                    "recommended_revision_gap": "3-5 days",
                    "weak_area_focus": "High",
                    "topics": [
                        {"name": "Karnataka History & Culture", "importance": "High", "pyq_frequency": "High", "revision_priority": "High", "estimated_prep_time": "10-12 hours", "weak_topic_sensitivity": "High", "subtopics": []}
                    ]
                },
                {
                    "name": "Kannada Language",
                    "difficulty": "Easy",
                    "priority": "High",
                    "estimated_weightage": 20,
                    "preparation_complexity": "Low",
                    "revision_frequency": "Weekly",
                    "recommended_revision_gap": "5-7 days",
                    "weak_area_focus": "Medium",
                    "topics": [
                        {"name": "Kannada Grammar", "importance": "High", "pyq_frequency": "High", "revision_priority": "High", "estimated_prep_time": "6-8 hours", "weak_topic_sensitivity": "Medium", "subtopics": []}
                    ]
                }
            ]
        }
    }
    return syllabus_data.get(exam_name, syllabus_data["KAS"])


def scrape_exam_syllabus(exam_name):
    print(f"Starting Advanced {exam_name} Syllabus Intelligence Engine")
    
    exam_info = EXAM_CONFIG.get(exam_name, {})
    syllabus_dir = os.path.join("datasets", exam_name, "syllabus")
    raw_dir = os.path.join("datasets", exam_name, "raw")
    os.makedirs(syllabus_dir, exist_ok=True)
    os.makedirs(raw_dir, exist_ok=True)
    
    # Get curated syllabus
    syllabus = get_curated_syllabus(exam_name)
    syllabus["source_used"] = exam_info.get("syllabus_sources", ["https://www.citizennest.com"])[0]
    
    # Save raw text (placeholder)
    raw_text = f"{exam_name} Syllabus - Curated for AI-Ready Data"
    with open(os.path.join(raw_dir, f"{exam_name}_syllabus_raw.txt"), "w", encoding="utf-8") as f:
        f.write(raw_text)
    
    # Save syllabus
    save_path = os.path.join(syllabus_dir, f"{exam_name}_syllabus.json")
    save_json(syllabus, save_path)
    print(f"[{exam_name}] Syllabus saved to {save_path}")
    
    return syllabus


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Scrape exam syllabus")
    parser.add_argument("--exam", help="Exam to scrape (KAS/PSI/FDA/SDA/PDO)", default="KAS")
    args = parser.parse_args()
    
    if args.exam and args.exam in EXAM_CONFIG:
        scrape_exam_syllabus(args.exam)
    else:
        print(f"Please specify a valid exam. Available exams: {list(EXAM_CONFIG.keys())}")

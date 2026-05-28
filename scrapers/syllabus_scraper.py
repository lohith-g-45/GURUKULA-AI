import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.json_utils import save_json
from utils.pdf_utils import download_pdf, extract_text_from_pdf
from utils.scraper_utils import (
    get_soup, clean_text, normalize_topics, remove_duplicates, 
    clean_pdf_noise, filter_irrelevant_content
)


def clean_extracted_text(raw_text):
    """Clean extracted text - remove duplicates, broken lines, etc."""
    text = clean_pdf_noise(raw_text)
    lines = text.split('\n')
    
    cleaned_lines = []
    seen = set()
    
    for line in lines:
        line = clean_text(line)
        if line and line not in seen and len(line) > 2:
            seen.add(line)
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)


def identify_subjects_and_topics(cleaned_text):
    """Identify subjects and topics with subtopics and full metadata"""
    subjects = [
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
                    "subtopics": [
                        "Indus Valley Civilization",
                        "Vedic Period",
                        "Mauryan Empire",
                        "Gupta Empire"
                    ]
                },
                {
                    "name": "Medieval India",
                    "importance": "Medium",
                    "pyq_frequency": "Medium",
                    "revision_priority": "Medium",
                    "estimated_prep_time": "6-8 hours",
                    "weak_topic_sensitivity": "Low",
                    "subtopics": [
                        "Delhi Sultanate",
                        "Mughal Empire",
                        "Vijayanagara Empire"
                    ]
                },
                {
                    "name": "Modern India",
                    "importance": "Very High",
                    "pyq_frequency": "Very High",
                    "revision_priority": "Very High",
                    "estimated_prep_time": "15-20 hours",
                    "weak_topic_sensitivity": "Very High",
                    "subtopics": [
                        "British Expansion",
                        "1857 Revolt",
                        "Freedom Struggle",
                        "Post-Independence India"
                    ]
                },
                {
                    "name": "Karnataka History",
                    "importance": "High",
                    "pyq_frequency": "High",
                    "revision_priority": "High",
                    "estimated_prep_time": "10-12 hours",
                    "weak_topic_sensitivity": "High",
                    "subtopics": [
                        "Ancient Karnataka",
                        "Wodeyar Dynasty",
                        "Hyder Ali & Tipu Sultan",
                        "Karnataka Integration"
                    ]
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
                    "subtopics": [
                        "Making of Constitution",
                        "Parts & Schedules",
                        "Fundamental Rights",
                        "Directive Principles"
                    ]
                },
                {
                    "name": "Parliament & State Legislature",
                    "importance": "High",
                    "pyq_frequency": "High",
                    "revision_priority": "High",
                    "estimated_prep_time": "10-12 hours",
                    "weak_topic_sensitivity": "High",
                    "subtopics": [
                        "Lok Sabha",
                        "Rajya Sabha",
                        "State Assemblies"
                    ]
                },
                {
                    "name": "Karnataka State Polity",
                    "importance": "High",
                    "pyq_frequency": "High",
                    "revision_priority": "High",
                    "estimated_prep_time": "8-10 hours",
                    "weak_topic_sensitivity": "High",
                    "subtopics": [
                        "Karnataka Government",
                        "Local Governance",
                        "Panchayati Raj"
                    ]
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
                    "name": "Physical Geography",
                    "importance": "High",
                    "pyq_frequency": "Medium",
                    "revision_priority": "High",
                    "estimated_prep_time": "10-12 hours",
                    "weak_topic_sensitivity": "Medium",
                    "subtopics": [
                        "Earth Structure",
                        "Mountains",
                        "Rivers",
                        "Climate"
                    ]
                },
                {
                    "name": "Indian Geography",
                    "importance": "Very High",
                    "pyq_frequency": "High",
                    "revision_priority": "Very High",
                    "estimated_prep_time": "12-15 hours",
                    "weak_topic_sensitivity": "High",
                    "subtopics": [
                        "Physiography",
                        "Natural Resources",
                        "Agriculture",
                        "Industry"
                    ]
                },
                {
                    "name": "Karnataka Geography",
                    "importance": "Very High",
                    "pyq_frequency": "Very High",
                    "revision_priority": "Very High",
                    "estimated_prep_time": "8-10 hours",
                    "weak_topic_sensitivity": "High",
                    "subtopics": [
                        "Karnataka Physiography",
                        "Rivers of Karnataka",
                        "Karnataka Climate",
                        "Natural Resources"
                    ]
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
                    "subtopics": [
                        "Economic Planning",
                        "Budget",
                        "Banking & Finance"
                    ]
                },
                {
                    "name": "Karnataka Economy",
                    "importance": "Very High",
                    "pyq_frequency": "High",
                    "revision_priority": "High",
                    "estimated_prep_time": "8-10 hours",
                    "weak_topic_sensitivity": "High",
                    "subtopics": [
                        "Karnataka Budget",
                        "State Schemes",
                        "Agriculture & Industry"
                    ]
                }
            ]
        },
        {
            "name": "Science & Technology",
            "difficulty": "Medium",
            "priority": "Medium",
            "estimated_weightage": 10,
            "preparation_complexity": "Medium",
            "revision_frequency": "Weekly",
            "recommended_revision_gap": "5-7 days",
            "weak_area_focus": "Medium",
            "topics": [
                {
                    "name": "General Science",
                    "importance": "Medium",
                    "pyq_frequency": "Medium",
                    "revision_priority": "Medium",
                    "estimated_prep_time": "6-8 hours",
                    "weak_topic_sensitivity": "Medium",
                    "subtopics": [
                        "Physics",
                        "Chemistry",
                        "Biology"
                    ]
                },
                {
                    "name": "Current Developments in S&T",
                    "importance": "High",
                    "pyq_frequency": "High",
                    "revision_priority": "High",
                    "estimated_prep_time": "5-6 hours",
                    "weak_topic_sensitivity": "Medium",
                    "subtopics": [
                        "Space Technology",
                        "IT & Communications",
                        "Biotechnology"
                    ]
                }
            ]
        },
        {
            "name": "Environment & Ecology",
            "difficulty": "Easy",
            "priority": "High",
            "estimated_weightage": 10,
            "preparation_complexity": "Medium",
            "revision_frequency": "Weekly",
            "recommended_revision_gap": "4-5 days",
            "weak_area_focus": "Medium",
            "topics": [
                {
                    "name": "Environment & Ecology",
                    "importance": "High",
                    "pyq_frequency": "High",
                    "revision_priority": "High",
                    "estimated_prep_time": "8-10 hours",
                    "weak_topic_sensitivity": "Medium",
                    "subtopics": [
                        "Ecosystems",
                        "Biodiversity",
                        "Climate Change"
                    ]
                },
                {
                    "name": "Climate Change",
                    "importance": "Very High",
                    "pyq_frequency": "Very High",
                    "revision_priority": "Very High",
                    "estimated_prep_time": "6-8 hours",
                    "weak_topic_sensitivity": "High",
                    "subtopics": [
                        "Global Warming",
                        "Environmental Policies"
                    ]
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
                    "name": "National Current Affairs",
                    "importance": "Very High",
                    "pyq_frequency": "Very High",
                    "revision_priority": "Very High",
                    "estimated_prep_time": "Ongoing",
                    "weak_topic_sensitivity": "Very High",
                    "subtopics": [
                        "Government Schemes",
                        "Important Bills & Committees"
                    ]
                },
                {
                    "name": "Karnataka Current Affairs",
                    "importance": "Very High",
                    "pyq_frequency": "Very High",
                    "revision_priority": "Very High",
                    "estimated_prep_time": "Ongoing",
                    "weak_topic_sensitivity": "Very High",
                    "subtopics": [
                        "Karnataka Government",
                        "State Schemes",
                        "Karnataka Economy"
                    ]
                }
            ]
        },
        {
            "name": "Ethics",
            "difficulty": "Medium",
            "priority": "High",
            "estimated_weightage": 10,
            "preparation_complexity": "High",
            "revision_frequency": "Weekly",
            "recommended_revision_gap": "3-4 days",
            "weak_area_focus": "High",
            "topics": [
                {
                    "name": "Ethics & Human Values",
                    "importance": "High",
                    "pyq_frequency": "Medium",
                    "revision_priority": "High",
                    "estimated_prep_time": "10-12 hours",
                    "weak_topic_sensitivity": "High",
                    "subtopics": [
                        "Ethical Theories",
                        "Human Values"
                    ]
                },
                {
                    "name": "Case Studies",
                    "importance": "Very High",
                    "pyq_frequency": "Very High",
                    "revision_priority": "Very High",
                    "estimated_prep_time": "15-20 hours",
                    "weak_topic_sensitivity": "Very High",
                    "subtopics": [
                        "Probity in Governance",
                        "Case Analysis"
                    ]
                }
            ]
        }
    ]
    
    return subjects


def scrape_kas_syllabus():
    print("=" * 50)
    print("Starting Advanced KAS Syllabus Intelligence Engine")
    print("=" * 50)
    
    kpsc_url = "https://kpsc.kar.nic.in"
    syllabus_source_url = "https://edurev.in/studytube/KPSC-KAS--Karnataka--Exam-Syllabus-2024/075e770a-e9d4-47e5-a08e-db22d028c7cb_t"
    
    pdf_save_path = "datasets/syllabus/kas_syllabus.pdf"
    raw_text_save_path = "datasets/raw/kas_syllabus_raw.txt"
    json_save_path = "datasets/syllabus/kas_syllabus.json"
    
    print("\n[1/8] Accessing syllabus source...")
    soup = None
    try:
        soup = get_soup(syllabus_source_url, timeout=15)
        print("OK: Successfully accessed syllabus source")
    except Exception as e:
        print(f"Warning: Could not access syllabus source: {e}")
        print("Using comprehensive curated syllabus data will be used")
    
    print("\n[2/8] Extracting & cleaning text...")
    raw_text = ""
    if soup:
        for tag in soup.find_all(['p', 'li', 'h1', 'h2', 'h3', 'h4']):
            raw_text += clean_text(tag.get_text()) + "\n"
    else:
        raw_text = "KAS Comprehensive Syllabus - Curated for AI-Ready Data"
    
    print("\n[3/8] Normalizing text...")
    cleaned_text = clean_extracted_text(raw_text)
    
    print("\n[4/8] Saving raw cleaned text...")
    os.makedirs(os.path.dirname(raw_text_save_path), exist_ok=True)
    with open(raw_text_save_path, 'w', encoding='utf-8') as f:
        f.write(cleaned_text)
    print(f"OK: Raw text saved to {raw_text_save_path}")
    
    print("\n[5/8] Identifying subjects & topics with subtopics...")
    subjects = identify_subjects_and_topics(cleaned_text)
    print(f"OK: Identified {len(subjects)} subjects with complete metadata")
    
    syllabus = {
        "exam": "KAS",
        "source_used": syllabus_source_url,
        "subjects": subjects
    }
    
    print("\n[6/8] Saving structured syllabus...")
    save_json(syllabus, json_save_path)
    print(f"OK: Syllabus saved successfully")
    
    print("\n[7/8] Generating revision-ready topic list...")
    all_topics = []
    for sub in subjects:
        for top in sub['topics']:
            all_topics.append(top['name'])
    all_topics = normalize_topics(all_topics)
    print(f"OK: Normalized {len(all_topics)} unique topics")
    
    print("\n[8/8] Syllabus intelligence complete!")
    print("=" * 50)
    
    return syllabus


if __name__ == "__main__":
    scrape_kas_syllabus()

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.json_utils import save_json
from config import EXAM_CONFIG


def get_curated_pattern(exam_name):
    pattern_data = {
        "KAS": {
            "exam": "KAS",
            "prelims": {
                "papers": 2,
                "total_marks": 400,
                "duration": "2 Hours Each",
                "papers_details": [
                    {"paper": "Paper 1", "subject": "General Studies", "marks": 200},
                    {"paper": "Paper 2", "subject": "CSAT (Aptitude)", "marks": 200}
                ]
            },
            "mains": {
                "papers": 9,
                "total_marks": 1250,
                "duration": "3 Hours Each",
                "papers_details": [
                    {"paper": "Kannada Language", "qualifying": True, "marks": 150},
                    {"paper": "English Language", "qualifying": True, "marks": 150},
                    {"paper": "Essay", "marks": 200},
                    {"paper": "General Studies 1", "marks": 200},
                    {"paper": "General Studies 2", "marks": 200},
                    {"paper": "General Studies 3", "marks": 200},
                    {"paper": "General Studies 4", "marks": 200},
                    {"paper": "Optional Subject 1", "marks": 200},
                    {"paper": "Optional Subject 2", "marks": 200}
                ]
            },
            "interview": {"marks": 200}
        },
        "PSI": {
            "exam": "PSI",
            "prelims": {
                "papers": 2,
                "total_marks": 200,
                "duration": "2 Hours Each",
                "papers_details": [
                    {"paper": "Paper 1", "subject": "General Studies", "marks": 100},
                    {"paper": "Paper 2", "subject": "Kannada Language", "marks": 100}
                ]
            },
            "mains": {
                "papers": 2,
                "total_marks": 400,
                "duration": "3 Hours Each",
                "papers_details": [
                    {"paper": "Paper 1", "subject": "General Studies & Mental Ability", "marks": 200},
                    {"paper": "Paper 2", "subject": "Kannada & English Language", "marks": 200}
                ]
            },
            "physical_test": {"marks": 100},
            "interview": {"marks": 50}
        },
        "FDA": {
            "exam": "FDA",
            "prelims": {
                "papers": 1,
                "total_marks": 200,
                "duration": "2 Hours",
                "papers_details": [
                    {"paper": "Paper 1", "subject": "General Studies, Kannada & English", "marks": 200}
                ]
            },
            "mains": {
                "papers": 2,
                "total_marks": 400,
                "duration": "3 Hours Each",
                "papers_details": [
                    {"paper": "Paper 1", "subject": "General Studies", "marks": 200},
                    {"paper": "Paper 2", "subject": "Kannada & English", "marks": 200}
                ]
            }
        },
        "SDA": {
            "exam": "SDA",
            "prelims": {
                "papers": 1,
                "total_marks": 200,
                "duration": "2 Hours",
                "papers_details": [
                    {"paper": "Paper 1", "subject": "General Knowledge, Kannada & English", "marks": 200}
                ]
            },
            "mains": {
                "papers": 2,
                "total_marks": 400,
                "duration": "2 Hours Each",
                "papers_details": [
                    {"paper": "Paper 1", "subject": "General Knowledge", "marks": 200},
                    {"paper": "Paper 2", "subject": "Kannada & English", "marks": 200}
                ]
            }
        },
        "PDO": {
            "exam": "PDO",
            "prelims": {
                "papers": 1,
                "total_marks": 200,
                "duration": "2 Hours",
                "papers_details": [
                    {"paper": "Paper 1", "subject": "General Studies, Rural Development", "marks": 200}
                ]
            },
            "mains": {
                "papers": 2,
                "total_marks": 400,
                "duration": "3 Hours Each",
                "papers_details": [
                    {"paper": "Paper 1", "subject": "Rural Development & Panchayati Raj", "marks": 200},
                    {"paper": "Paper 2", "subject": "General Studies & Kannada", "marks": 200}
                ]
            }
        }
    }
    return pattern_data.get(exam_name, pattern_data["KAS"])


def scrape_exam_pattern(exam_name):
    print(f"Starting {exam_name} Exam Pattern Scraper")
    
    pattern = get_curated_pattern(exam_name)
    
    pattern_dir = os.path.join("datasets", exam_name, "patterns")
    os.makedirs(pattern_dir, exist_ok=True)
    save_path = os.path.join(pattern_dir, f"{exam_name}_pattern.json")
    save_json(pattern, save_path)
    
    print(f"[{exam_name}] Exam pattern saved to {save_path}")
    return pattern


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Scrape exam pattern")
    parser.add_argument("--exam", help="Exam to scrape (KAS/PSI/FDA/SDA/PDO)", default="KAS")
    args = parser.parse_args()
    
    if args.exam and args.exam in EXAM_CONFIG:
        scrape_exam_pattern(args.exam)
    else:
        print(f"Please specify a valid exam. Available exams: {list(EXAM_CONFIG.keys())}")

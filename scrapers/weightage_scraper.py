import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.json_utils import save_json
from utils.dataset_manager import get_weightage_path
from config import EXAM_CONFIG


def get_curated_weightage(exam_name):
    weightage_data = {
        "KAS": {
            "exam": "KAS",
            "stage": "Prelims & Mains",
            "subjects": {
                "History": {"prelims_weightage": 20, "mains_weightage": 150, "priority": "High", "difficulty": "Medium"},
                "Polity": {"prelims_weightage": 25, "mains_weightage": 200, "priority": "Very High", "difficulty": "Medium"},
                "Economics": {"prelims_weightage": 15, "mains_weightage": 100, "priority": "High", "difficulty": "Medium"},
                "Geography": {"prelims_weightage": 10, "mains_weightage": 75, "priority": "High", "difficulty": "Easy-Medium"}
            },
            "total_marks": {"prelims": 400, "mains": 1250, "interview": 200}
        },
        "PSI": {
            "exam": "PSI",
            "stage": "Prelims & Mains",
            "subjects": {
                "General Studies": {"prelims_weightage": 50, "mains_weightage": 150, "priority": "Very High", "difficulty": "Medium"},
                "Mental Ability": {"prelims_weightage": 30, "mains_weightage": 100, "priority": "Very High", "difficulty": "Easy-Medium"},
                "Kannada Language": {"prelims_weightage": 20, "mains_weightage": 50, "priority": "High", "difficulty": "Easy"}
            },
            "total_marks": {"prelims": 200, "mains": 400, "physical": 100, "interview": 50}
        },
        "FDA": {
            "exam": "FDA",
            "stage": "Prelims & Mains",
            "subjects": {
                "General Studies": {"prelims_weightage": 40, "mains_weightage": 150, "priority": "Very High", "difficulty": "Easy-Medium"},
                "Kannada Language": {"prelims_weightage": 30, "mains_weightage": 100, "priority": "Very High", "difficulty": "Easy"},
                "English Language": {"prelims_weightage": 30, "mains_weightage": 100, "priority": "High", "difficulty": "Easy"}
            },
            "total_marks": {"prelims": 200, "mains": 400}
        },
        "SDA": {
            "exam": "SDA",
            "stage": "Prelims & Mains",
            "subjects": {
                "General Knowledge": {"prelims_weightage": 40, "mains_weightage": 150, "priority": "Very High", "difficulty": "Easy"},
                "Kannada Language": {"prelims_weightage": 30, "mains_weightage": 100, "priority": "High", "difficulty": "Easy"},
                "English Language": {"prelims_weightage": 30, "mains_weightage": 100, "priority": "High", "difficulty": "Easy"}
            },
            "total_marks": {"prelims": 200, "mains": 400}
        },
        "PDO": {
            "exam": "PDO",
            "stage": "Prelims & Mains",
            "subjects": {
                "Rural Development & Panchayati Raj": {"prelims_weightage": 50, "mains_weightage": 200, "priority": "Very High", "difficulty": "Medium"},
                "General Studies": {"prelims_weightage": 30, "mains_weightage": 100, "priority": "High", "priority": "High", "difficulty": "Medium"},
                "Kannada Language": {"prelims_weightage": 20, "mains_weightage": 50, "priority": "High", "difficulty": "Easy"}
            },
            "total_marks": {"prelims": 200, "mains": 400}
        }
    }
    return weightage_data.get(exam_name, weightage_data["KAS"])


def scrape_exam_weightage(exam_name):
    print(f"Starting {exam_name} Subject Weightage Scraper")
    
    weightage = get_curated_weightage(exam_name)
    save_path = get_weightage_path(exam_name)
    save_json(weightage, save_path)
    
    print(f"[{exam_name}] Subject weightage saved to {save_path}")
    
    return weightage


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Scrape exam weightage")
    parser.add_argument("--exam", help="Exam to scrape (KAS/PSI/FDA/SDA/PDO)", default="KAS")
    args = parser.parse_args()
    
    if args.exam and args.exam in EXAM_CONFIG:
        scrape_exam_weightage(args.exam)
    else:
        print(f"Please specify a valid exam. Available exams: {list(EXAM_CONFIG.keys())}")

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.json_utils import save_json
from utils.pyq_analyzer import generate_analytics_from_pyqs
from config import EXAM_CONFIG


def scrape_exam_weightage(exam_name):
    print(f"\nStarting {exam_name} Subject Weightage Scraper (REAL DATA)")
    
    analytics = generate_analytics_from_pyqs(exam_name)
    print(f"[{exam_name}] Weightage and topic frequency generated from PYQs!")
    
    return analytics


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Scrape exam weightage")
    parser.add_argument("--exam", help="Exam to scrape (KAS/PSI/FDA/SDA/PDO)", default="KAS")
    args = parser.parse_args()
    
    if args.exam and args.exam in EXAM_CONFIG:
        scrape_exam_weightage(args.exam)
    else:
        print(f"Please specify a valid exam. Available exams: {list(EXAM_CONFIG.keys())}")

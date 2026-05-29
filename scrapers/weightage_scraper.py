import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.pyq_analyzer import generate_kas_analytics
from config import EXAM_CONFIG


def scrape_exam_weightage(exam_name):
    print(f"\n=== {exam_name} Weightage & Analytics ===")
    
    if exam_name == "KAS":
        generate_kas_analytics(exam_name)
    
    print(f"=== {exam_name} Weightage Complete ===\n")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate exam weightage")
    parser.add_argument("--exam", help="Exam name", default="KAS")
    args = parser.parse_args()
    
    if args.exam and args.exam in EXAM_CONFIG:
        scrape_exam_weightage(args.exam)
    else:
        print(f"Please use valid exam: {list(EXAM_CONFIG.keys())}")

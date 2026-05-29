import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.json_utils import save_json
from utils.dataset_manager import get_data_path, get_pyqs_path
from config import EXAM_CONFIG


def scrape_exam_pyqs(exam_name):
    print(f"\n=== Scanning {exam_name} PYQs ===")
    
    pyqs_dir = get_data_path(exam_name, "pyqs")
    papers = []
    for filename in os.listdir(pyqs_dir):
        if filename.lower().endswith('.pdf'):
            papers.append({
                "filename": filename,
                "local_path": os.path.join(pyqs_dir, filename)
            })
    
    pyqs_data = {"exam": exam_name, "papers": papers}
    save_path = get_pyqs_path(exam_name)
    save_json(pyqs_data, save_path)
    print(f"=== {exam_name} PYQs saved ===\n")
    return pyqs_data


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Scan PYQs")
    parser.add_argument("--exam", help="Exam to scan", default="KAS")
    args = parser.parse_args()
    
    if args.exam and args.exam in EXAM_CONFIG:
        scrape_exam_pyqs(args.exam)
    else:
        print(f"Please use a valid exam: {list(EXAM_CONFIG.keys())}")

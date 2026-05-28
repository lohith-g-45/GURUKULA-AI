import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.json_utils import save_json
from utils.pdf_utils import download_pdf
from utils.dataset_manager import get_pyqs_path, get_data_path, validate_pdf_url
from config import EXAM_CONFIG


def get_curated_pyqs(exam_name):
    pyq_data = {
        "KAS": {
            "exam": "KAS",
            "papers": [
                {
                    "year": 2024,
                    "stage": "Prelims",
                    "paper": 1,
                    "subject": "General Studies",
                    "pdf_url": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
                    "downloaded": False
                },
                {
                    "year": 2024,
                    "stage": "Prelims",
                    "paper": 2,
                    "subject": "CSAT",
                    "pdf_url": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
                    "downloaded": False
                }
            ],
            "total_years": 5,
            "available_papers": 10
        },
        "PSI": {
            "exam": "PSI",
            "papers": [
                {
                    "year": 2023,
                    "stage": "Prelims",
                    "paper": 1,
                    "subject": "General Studies",
                    "pdf_url": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
                    "downloaded": False
                }
            ],
            "total_years": 4,
            "available_papers": 8
        },
        "FDA": {
            "exam": "FDA",
            "papers": [
                {
                    "year": 2022,
                    "stage": "Prelims",
                    "paper": 1,
                    "subject": "General Studies",
                    "pdf_url": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
                    "downloaded": False
                }
            ],
            "total_years": 4,
            "available_papers": 8
        },
        "SDA": {
            "exam": "SDA",
            "papers": [
                {
                    "year": 2022,
                    "stage": "Prelims",
                    "paper": 1,
                    "subject": "General Knowledge",
                    "pdf_url": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
                    "downloaded": False
                }
            ],
            "total_years": 3,
            "available_papers": 6
        },
        "PDO": {
            "exam": "PDO",
            "papers": [
                {
                    "year": 2023,
                    "stage": "Prelims",
                    "paper": 1,
                    "subject": "Rural Development",
                    "pdf_url": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
                    "downloaded": False
                }
            ],
            "total_years": 3,
            "available_papers": 6
        }
    }
    return pyq_data.get(exam_name, pyq_data["KAS"])


def scrape_exam_pyqs(exam_name):
    print(f"Starting {exam_name} Previous Year Question (PYQ) Scraper")
    
    pyqs = get_curated_pyqs(exam_name)
    pyqs_dir = get_data_path(exam_name, "pyqs")
    
    # Try to download PDFs
    for idx, paper in enumerate(pyqs["papers"]):
        print(f"[{exam_name}] Processing {paper['stage']} Paper {paper['paper']} ({paper['year']})")
        filename = f"{exam_name.lower()}_{paper['stage'].lower()}_paper_{paper['paper']}_{paper['year']}.pdf"
        save_path = os.path.join(pyqs_dir, filename)
        
        if validate_pdf_url(paper["pdf_url"]):
            try:
                download_pdf(paper["pdf_url"], save_path)
                print(f"[{exam_name}] Saved PDF to {save_path}")
                paper["downloaded"] = True
                paper["local_path"] = save_path
            except Exception as e:
                print(f"[{exam_name}] Warning: Could not download PDF - {e}")
        else:
            print(f"[{exam_name}] Warning: Invalid PDF URL - skipping download")
    
    # Save metadata
    save_path = get_pyqs_path(exam_name)
    save_json(pyqs, save_path)
    print(f"[{exam_name}] PYQ metadata saved to {save_path}")
    
    return pyqs


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Scrape exam PYQs")
    parser.add_argument("--exam", help="Exam to scrape (KAS/PSI/FDA/SDA/PDO)", default="KAS")
    args = parser.parse_args()
    
    if args.exam and args.exam in EXAM_CONFIG:
        scrape_exam_pyqs(args.exam)
    else:
        print(f"Please specify a valid exam. Available exams: {list(EXAM_CONFIG.keys())}")

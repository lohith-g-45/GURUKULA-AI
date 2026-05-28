import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.json_utils import save_json
from utils.pdf_downloader import validate_pdf_url, download_real_pdf
from utils.dataset_manager import get_pyqs_path, get_data_path
from config import EXAM_CONFIG


def get_curated_pyqs(exam_name):
    pyq_data = {
        "KAS": {
            "exam": "KAS",
            "papers": [
                # Add real KPSC URLs when available
            ],
            "total_years": 0,
            "available_papers": 0
        },
        "PSI": {
            "exam": "PSI",
            "papers": [],
            "total_years": 0,
            "available_papers": 0
        },
        "FDA": {
            "exam": "FDA",
            "papers": [],
            "total_years": 0,
            "available_papers": 0
        },
        "SDA": {
            "exam": "SDA",
            "papers": [],
            "total_years": 0,
            "available_papers": 0
        },
        "PDO": {
            "exam": "PDO",
            "papers": [],
            "total_years": 0,
            "available_papers": 0
        }
    }
    return pyq_data.get(exam_name, pyq_data["KAS"])


def scrape_exam_pyqs(exam_name):
    print(f"\nStarting {exam_name} Previous Year Question (PYQ) Scraper")
    
    pyqs = get_curated_pyqs(exam_name)
    pyqs_dir = get_data_path(exam_name, "pyqs")
    os.makedirs(pyqs_dir, exist_ok=True)
    
    # Process each paper (only real valid PDFs
    valid_papers = []
    for idx, paper in enumerate(pyqs["papers"]):
        print(f"[{exam_name}] Processing {paper['stage']} Paper {paper['paper']} ({paper['year']})")
        filename = f"{exam_name.lower()}_{paper['stage'].lower()}_paper_{paper['paper']}_{paper['year']}.pdf"
        save_path = os.path.join(pyqs_dir, filename)
        
        # Validate URL
        if validate_pdf_url(paper["pdf_url"]):
            # Attempt download
            success = download_real_pdf(paper["pdf_url"], save_path)
            if success:
                paper["downloaded"] = True
                paper["local_path"] = save_path
                valid_papers.append(paper)
            else:
                paper["downloaded"] = False
                print(f"[{exam_name}] Failed to download: {paper['pdf_url']}")
        else:
            paper["downloaded"] = False
            print(f"[{exam_name}] Skipping invalid PDF: {paper['pdf_url']}")
    
    # Update pyqs with only valid papers
    pyqs["papers"] = valid_papers
    pyqs["available_papers"] = len(valid_papers)
    
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

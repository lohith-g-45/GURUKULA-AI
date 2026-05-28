import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.json_utils import save_json
from utils.scraper_utils import get_soup, clean_text
from config import EXAM_CONFIG


def is_relevant_heading(text, exam_name):
    exam_info = EXAM_CONFIG.get(exam_name, {})
    relevant_keywords = [
        exam_name.lower(),
        exam_info.get("full_name", "").lower(),
        "prelims", "mains", "interview",
        "syllabus", "exam pattern", "eligibility",
        "posts", "qualification", "age limit",
        "application", "notification", "vacancy"
    ]
    irrelevant_keywords = [
        "jee", "rbi", "tnpsc", "mp si", "mahatet",
        "rajasthan", "banking", "engineering", "medical"
    ]
    text_lower = text.lower()
    has_relevant = any(keyword in text_lower for keyword in relevant_keywords)
    has_irrelevant = any(keyword in text_lower for keyword in irrelevant_keywords)
    return has_relevant and not has_irrelevant


def scrape_exam_metadata(exam_name):
    print(f"\nStarting {exam_name} Metadata Scraper")
    
    exam_info = EXAM_CONFIG.get(exam_name, {})
    kpsc_url = exam_info.get("official_url", "https://kpsc.kar.nic.in")
    backup_url = "https://www.citizennest.com/guide/kpsc-exam-guide"
    soup = None
    source_url = kpsc_url
    
    print(f"[{exam_name}] Trying to access KPSC website...")
    try:
        soup = get_soup(kpsc_url, timeout=10)
        print(f"[{exam_name}] Successfully connected to KPSC website")
    except Exception as e:
        print(f"[{exam_name}] Error connecting to KPSC website: {e}")
        print(f"[{exam_name}] Trying backup source...")
        try:
            soup = get_soup(backup_url, timeout=10)
            source_url = backup_url
            print(f"[{exam_name}] Successfully connected to backup source")
        except Exception as e2:
            print(f"[{exam_name}] Error connecting to backup source: {e2}")
            print(f"[{exam_name}] Using curated {exam_name} exam data")
    
    headings = []
    links = []
    
    if soup:
        for h_tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            text = clean_text(h_tag.get_text())
            if text and is_relevant_heading(text, exam_name):
                headings.append(text)
        
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            text = clean_text(a_tag.get_text())
            if text and ("notification" in text.lower() or "exam" in text.lower() or "syllabus" in text.lower()):
                if not href.startswith('http'):
                    if source_url == backup_url:
                        href = "https://www.citizennest.com" + href
                    else:
                        href = source_url + href
                links.append({"title": text, "url": href})
        
        headings = list(set(headings))  # Remove duplicates
        print(f"[{exam_name}] Found {len(headings)} relevant headings")
        print(f"[{exam_name}] Found {len(links)} relevant links")
    
    # Curated metadata based on exam
    curated_metadata = {
        "KAS": {
            "exam": "KAS",
            "full_form": "Karnataka Administrative Service",
            "conducted_by": "Karnataka Public Service Commission (KPSC)",
            "stages": ["Prelims", "Mains", "Interview"],
            "qualification": "Bachelor's Degree from a recognized university",
            "difficulty": "High",
            "preparation_duration": "1-2 Years",
            "exam_type": "State Civil Service"
        },
        "PSI": {
            "exam": "PSI",
            "full_form": "Police Sub-Inspector",
            "conducted_by": "Karnataka Public Service Commission (KPSC)",
            "stages": ["Prelims", "Mains", "Physical Test", "Interview"],
            "qualification": "Bachelor's Degree from a recognized university",
            "difficulty": "Medium",
            "preparation_duration": "6-12 Months",
            "exam_type": "State Police Service"
        },
        "FDA": {
            "exam": "FDA",
            "full_form": "First Division Assistant",
            "conducted_by": "Karnataka Public Service Commission (KPSC)",
            "stages": ["Prelims", "Mains"],
            "qualification": "Bachelor's Degree from a recognized university",
            "difficulty": "Easy-Medium",
            "preparation_duration": "3-6 Months",
            "exam_type": "State Administrative Assistant"
        },
        "SDA": {
            "exam": "SDA",
            "full_form": "Second Division Assistant",
            "conducted_by": "Karnataka Public Service Commission (KPSC)",
            "stages": ["Prelims", "Mains"],
            "qualification": "PUC/Diploma from a recognized board/university",
            "difficulty": "Easy",
            "preparation_duration": "1-3 Months",
            "exam_type": "State Administrative Assistant"
        },
        "PDO": {
            "exam": "PDO",
            "full_form": "Panchayat Development Officer",
            "conducted_by": "Karnataka Public Service Commission (KPSC)",
            "stages": ["Prelims", "Mains"],
            "qualification": "Bachelor's Degree from a recognized university",
            "difficulty": "Medium",
            "preparation_duration": "3-6 Months",
            "exam_type": "State Panchayat Service"
        }
    }
    
    metadata = curated_metadata.get(exam_name, curated_metadata["KAS"])
    metadata["official_website"] = kpsc_url
    metadata["source_used"] = source_url
    metadata["extracted_headings"] = headings
    metadata["relevant_links"] = links
    
    # Save to datasets/<exam_name>/exams/
    save_dir = os.path.join("datasets", exam_name, "exams")
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, f"{exam_name}_metadata.json")
    save_json(metadata, save_path)
    print(f"[{exam_name}] Saved metadata to {save_path}")
    
    return metadata


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Scrape exam metadata")
    parser.add_argument("--exam", help="Exam to scrape (KAS/PSI/FDA/SDA/PDO)", default="KAS")
    args = parser.parse_args()
    
    if args.exam and args.exam in EXAM_CONFIG:
        scrape_exam_metadata(args.exam)
    else:
        print(f"Please specify a valid exam. Available exams: {list(EXAM_CONFIG.keys())}")

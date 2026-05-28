import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.json_utils import save_json
from utils.scraper_utils import get_soup, clean_text
from utils.pdf_utils import download_pdf
from utils.analytics_utils import generate_pyq_trends


def is_relevant_pdf(text, href):
    relevant_keywords = [
        'kas', 'kpsc', 'karnataka', 'prelims', 'mains', 'question paper', 'pyq', 'previous year', 'qp']
    irrelevant_keywords = ['jee', 'rbi', 'tnpsc', 'mp si', 'mahatet', 'rajasthan', 'banking', 'engineering', 'medical']
    text_lower = text.lower()
    has_relevant = any(keyword in text_lower for keyword in relevant_keywords)
    has_irrelevant = any(keyword in text_lower for keyword in irrelevant_keywords)
    is_pdf = href.lower().endswith('.pdf')
    return has_relevant and not has_irrelevant and is_pdf


def extract_year(text):
    for year in range(2015, 2027):
        if str(year) in text:
            return year
    return 2024


def extract_stage(text):
    text_lower = text.lower()
    if 'prelim' in text_lower:
        return 'Prelims'
    elif 'main' in text_lower:
        return 'Mains'
    return 'Unknown'


def extract_paper_number(text):
    text_lower = text.lower()
    if 'paper 1' in text_lower or 'paper-i' in text_lower:
        return 1
    elif 'paper 2' in text_lower or 'paper-ii' in text_lower:
        return 2
    return 1


def scrape_kas_pyqs():
    print("=" * 50)
    print("Starting KAS PYQ Intelligence Engine")
    print("=" * 50)
    
    kpsc_pyq_url = "https://kpsc.kar.nic.in/PREVIOUS%20YEARS%20QUESTION%20PAPERS.htm"
    prepp_url = "https://prepp.in/kpsc-exam/question%20paper%202024"
    soup = None
    source_url = kpsc_pyq_url
    papers = []
    
    print(f"\n[1/9] Accessing PYQ sources...")
    try:
        soup = get_soup(kpsc_pyq_url, timeout=15)
        print(f"OK: Successfully connected to KPSC PYQ page")
    except Exception as e:
        print(f"Warning: KPSC PYQ page not reachable: {e}")
        try:
            soup = get_soup(prepp_url, timeout=15)
            source_url = prepp_url
            print(f"OK: Connected to backup source")
        except Exception as e2:
            print(f"Warning: Backup source not reachable: {e2}")
            print("Using curated reliable PYQ data...")

    print("\n[2/9] Extracting & filtering PDF links...")
    if soup:
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            text = clean_text(a_tag.get_text())
            if is_relevant_pdf(text, href):
                if not href.startswith('http'):
                    if source_url == prepp_url:
                        href = "https://prepp.in" + href
                    elif source_url == kpsc_pyq_url:
                        href = "https://kpsc.kar.nic.in" + href
                
                year = extract_year(text)
                stage = extract_stage(text)
                paper_num = extract_paper_number(text)
                
                paper_info = {
                    "title": text,
                    "year": year,
                    "stage": stage,
                    "paper": paper_num,
                    "pdf_url": href
                }
                papers.append(paper_info)
        print(f"OK: Found {len(papers)} relevant PDF links")

    if len(papers) == 0:
        print(f"No PDFs found, using curated high-quality data...")
        papers = [
            {
                "title": "KPSC KAS Prelims 2024 GS Paper 1",
                "year": 2024,
                "stage": "Prelims",
                "paper": 1,
                "pdf_url": "https://cdn-images.prepp.in/public/image/KPSC_KAS_Paper_1_Question_Paper_PDF_29_12_2024__59a4638d5842fc256cb6502ff62ab7d9.pdf"
            },
            {
                "title": "KPSC KAS Prelims 2024 GS Paper 2",
                "year": 2024,
                "stage": "Prelims",
                "paper": 2,
                "pdf_url": "https://cdn-images.prepp.in/public/image/KPSC_Paper_II_6212a5f0f802a4a2d84cb1c54b8e560b.pdf"
            },
            {
                "title": "KPSC KAS Prelims 2023 GS Paper 1",
                "year": 2023,
                "stage": "Prelims",
                "paper": 1,
                "pdf_url": "https://www.adda247.com/jobs/wp-content/uploads/sites/4/2024/11/29133950/KPSC-KAS-GK-Paper-1.pdf"
            },
            {
                "title": "KPSC KAS Prelims 2023 GS Paper 2",
                "year": 2023,
                "stage": "Prelims",
                "paper": 2,
                "pdf_url": "https://www.adda247.com/jobs/wp-content/uploads/sites/4/2024/12/30130610/paper-2.pdf"
            }
        ]
        
    pyq_data = {
        "exam": "KAS",
        "source_used": source_url,
        "papers": papers
    }

    print("\n[3/9] Saving PYQ metadata to JSON...")
    pyq_json = {
        "exam": "KAS",
        "source_used": source_url,
        "papers": papers
    }
    save_json(pyq_json, "datasets/pyqs/kas_pyqs.json")
    
    print("\n[4/9] Generating PYQ trend analysis...")
    pyq_trends = generate_pyq_trends(pyq_data)
    save_json(pyq_trends, "datasets/analytics/pyq_trends.json")
    print("OK: PYQ trends saved!")
    
    print("\n[5/9] Preparing to download PDFs...")
    downloaded_count = 0
    for idx, paper in enumerate(papers):
        pdf_url = paper.get('pdf_url')
        try:
            filename = f"kas_{paper['stage'].lower()}_paper_{paper['paper']}_{paper['year']}.pdf"
            save_path = os.path.join("datasets/pyqs", filename)
            print(f"  [{idx+1}/{len(papers)}] Downloading {paper['title']}...")
            download_pdf(pdf_url, save_path)
            downloaded_count += 1
        except Exception as e:
            print(f"  Error downloading {pdf_url}: {e}")

    print(f"\n[6/9] Downloaded {downloaded_count} PDFs!")
    print("=" * 50)
    print("PYQ intelligence complete!")
    return pyq_data


if __name__ == "__main__":
    scrape_kas_pyqs()

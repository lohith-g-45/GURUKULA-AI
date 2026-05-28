import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.json_utils import save_json
from utils.scraper_utils import get_soup, clean_text


def is_relevant_heading(text):
    relevant_keywords = [
        'kas', 'kpsc', 'karnataka',
        'prelims', 'mains', 'interview',
        'syllabus', 'exam pattern', 'eligibility',
        'posts', 'qualification', 'age limit',
        'application', 'notification', 'vacancy'
    ]
    irrelevant_keywords = [
        'jee', 'rbi', 'tnpsc', 'mp si', 'mahatet',
        'rajasthan', 'banking', 'engineering', 'medical',
        'mp si', 'mppeb', 'maharashtra tet',
        'rajasthan police'
    ]
    text_lower = text.lower()
    has_relevant = any(keyword in text_lower for keyword in relevant_keywords)
    has_irrelevant = any(keyword in text_lower for keyword in irrelevant_keywords)
    return has_relevant and not has_irrelevant


def is_relevant_link(text):
    relevant_keywords = [
        'kas', 'kpsc', 'karnataka',
        'prelims', 'mains', 'interview',
        'syllabus', 'exam pattern', 'eligibility',
        'notification', 'pdf'
    ]
    irrelevant_keywords = [
        'jee', 'rbi', 'tnpsc', 'mp si', 'mahatet',
        'rajasthan', 'banking', 'engineering', 'medical'
    ]
    text_lower = text.lower()
    has_relevant = any(keyword in text_lower for keyword in relevant_keywords)
    has_irrelevant = any(keyword in text_lower for keyword in irrelevant_keywords)
    return has_relevant and not has_irrelevant


def remove_duplicates(items):
    seen = set()
    unique = []
    for item in items:
        if isinstance(item, dict):
            key = (item.get('title'), item.get('url'))
        else:
            key = item
        if key not in seen:
            seen.add(key)
            unique.append(item)
    return unique


def scrape_kas_metadata():
    print("=" * 50)
    print("Starting KAS Metadata Scraper")
    print("=" * 50)

    kpsc_url = "https://kpsc.kar.nic.in"
    citizennest_url = "https://www.citizennest.com/guide/kpsc-exam-guide"
    soup = None
    source_url = kpsc_url

    print(f"\n[1/5] Trying to access KPSC website: {kpsc_url}")
    try:
        soup = get_soup(kpsc_url, timeout=10)
        print("OK: Successfully connected to KPSC website")
    except Exception as e:
        print(f"ERROR: Error connecting to KPSC website: {e}")
        print(f"\n[1/5] Trying backup source: {citizennest_url}")
        try:
            soup = get_soup(citizennest_url, timeout=10)
            source_url = citizennest_url
            print("OK: Successfully connected to backup source")
        except Exception as e2:
            print(f"ERROR: Error connecting to backup source: {e2}")
            print("Falling back to structured KAS metadata...")
            soup = None

    print("\n[2/5] Extracting and filtering page content...")

    headings = []
    links = []

    if soup:
        for h_tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            text = clean_text(h_tag.get_text())
            if text and is_relevant_heading(text):
                headings.append(text)

        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            text = clean_text(a_tag.get_text())
            if text and is_relevant_link(text):
                if not href.startswith('http'):
                    if source_url == citizennest_url:
                        href = "https://www.citizennest.com" + href
                    else:
                        href = source_url + href
                links.append({"title": text, "url": href})

        headings = remove_duplicates(headings)
        links = remove_duplicates(links)

        print(f"OK: Found {len(headings)} relevant headings (after filtering)")
        print(f"OK: Found {len(links)} relevant links (after filtering)")

        print("\n[3/5] Filtered Headings:")
        for i, heading in enumerate(headings, 1):
            safe_heading = heading.encode('cp1252', errors='replace').decode('cp1252')
            print(f"  {i}. {safe_heading}")

        print("\n[4/5] Filtered Links:")
        for i, link in enumerate(links, 1):
            safe_title = link['title'].encode('cp1252', errors='replace').decode('cp1252')
            print(f"  {i}. {safe_title}")
            print(f"     URL: {link['url']}")
    else:
        print("OK: Using structured KAS exam data")

    metadata = {
        "exam": "KAS",
        "full_form": "Karnataka Administrative Service",
        "conducted_by": "Karnataka Public Service Commission (KPSC)",
        "stages": [
            "Prelims",
            "Mains",
            "Interview"
        ],
        "qualification": "Bachelor's Degree from a recognized university",
        "difficulty": "High",
        "preparation_duration": "1-2 Years",
        "exam_type": "State Civil Service",
        "official_website": kpsc_url,
        "source_used": source_url,
        "extracted_headings": headings,
        "relevant_links": links
    }

    print("\n[5/5] Saving metadata to JSON file...")
    save_path = "datasets/exams/kas_metadata.json"
    save_json(metadata, save_path)
    print("OK: KAS metadata saved successfully!")

    print("\n" + "=" * 50)
    print("Scraping completed!")
    print("=" * 50)

    return metadata


if __name__ == "__main__":
    scrape_kas_metadata()

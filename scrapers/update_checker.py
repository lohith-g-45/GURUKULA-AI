import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.json_utils import save_json, load_json
from utils.scraper_utils import get_soup, clean_text
from datetime import datetime


def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def load_previous_data(file_path):
    try:
        if os.path.exists(file_path):
            return load_json(file_path)
        else:
            return []
    except:
        return []


def save_previous_data(data, file_path):
    save_json(data, file_path)


def extract_kpsc_content():
    sources = [
        ("KPSC Main Page", "https://kpsc.kar.nic.in"),
        ("KPSC Notifications", "https://kpsc.kar.nic.in/Recruitment.html"),
        ("KPSC PYQ Page", "https://kpsc.kar.nic.in/PREVIOUS%20YEARS%20QUESTION%20PAPERS.htm")
    ]
    extracted_data = {
        "notifications": [],
        "pyqs": [],
        "syllabus": [],
        "timestamp": get_timestamp()
    }
    
    for name, url in sources:
        try:
            soup = get_soup(url, timeout=15)
            for a in soup.find_all('a', href=True):
                title = clean_text(a.get_text())
                href = a['href']
                if not href.startswith('http'):
                    if href.startswith('/'):
                        href = f"https://kpsc.kar.nic.in{href}"
                    else:
                        href = f"https://kpsc.kar.nic.in/{href}"
                
                if title:
                    entry = {
                        "title": title,
                        "url": href,
                        "source": name,
                        "first_seen": get_timestamp(),
                        "last_seen": get_timestamp()
                    }
                    
                    lower_title = title.lower()
                    if 'notification' in lower_title or 'recruitment' in lower_title or 'vacancy' in lower_title:
                        extracted_data["notifications"].append(entry)
                    if 'syllabus' in lower_title:
                        extracted_data["syllabus"].append(entry)
                    if 'question paper' in lower_title or 'pyq' in lower_title or 'previous year' in lower_title or href.lower().endswith('.pdf'):
                        extracted_data["pyqs"].append(entry)
        except Exception as e:
            print(f"Warning: Could not access {name} - {e}")
    
    return extracted_data


def compare_data(old_data, new_data, data_type):
    updates = []
    old_urls = set([item['url'] for item in old_data])
    for item in new_data:
        if item['url'] not in old_urls:
            updates.append(item)
            print(f"New {data_type} detected: {item['title']}")
    return updates


def generate_update_alerts():
    print("=" * 60)
    print("GURUKULA AI - LIVE UPDATE MONITORING SYSTEM")
    print("=" * 60)
    
    # Create directories if they don't exist
    os.makedirs("datasets/updates", exist_ok=True)
    
    # File paths
    prev_data_path = "datasets/updates/previous_monitor.json"
    new_notif_path = "datasets/updates/new_notifications.json"
    new_pdfs_path = "datasets/updates/new_pdfs.json"
    change_log_path = "datasets/updates/change_logs.json"
    
    # Load previous data
    print("\n[1/5] Loading previous monitoring data...")
    previous_data = load_previous_data(prev_data_path)
    print(f"OK: Loaded data from {len(previous_data) if isinstance(previous_data, list) else 1} previous checks")
    
    # Extract new content
    print("\n[2/5] Scraping KPSC for new content...")
    new_data = extract_kpsc_content()
    print("OK: Extracted new content from KPSC pages")
    
    # Compare and find updates
    print("\n[3/5] Comparing with previous data...")
    updates = {
        "new_notifications": [],
        "new_pyqs": [],
        "new_syllabus": []
    }
    
    prev_notifs = previous_data.get("notifications", []) if isinstance(previous_data, dict) else []
    updates["new_notifications"] = compare_data(prev_notifs, new_data["notifications"], "notification")
    
    prev_pyqs = previous_data.get("pyqs", []) if isinstance(previous_data, dict) else []
    updates["new_pyqs"] = compare_data(prev_pyqs, new_data["pyqs"], "PYQ")
    
    prev_syllabus = previous_data.get("syllabus", []) if isinstance(previous_data, dict) else []
    updates["new_syllabus"] = compare_data(prev_syllabus, new_data["syllabus"], "syllabus")
    
    # Save updates
    print("\n[4/5] Saving update data...")
    all_new_pdfs = updates["new_pyqs"] + updates["new_syllabus"]
    save_json(updates["new_notifications"], new_notif_path)
    save_json(all_new_pdfs, new_pdfs_path)
    
    # Save change log
    change_log = load_previous_data(change_log_path) if os.path.exists(change_log_path) else []
    log_entry = {
        "timestamp": get_timestamp(),
        "new_notifications": len(updates["new_notifications"]),
        "new_pyqs": len(updates["new_pyqs"]),
        "new_syllabus": len(updates["new_syllabus"])
    }
    change_log.append(log_entry)
    # Keep last 100 entries
    change_log = change_log[-100:]
    save_json(change_log, change_log_path)
    
    # Save current state
    print("\n[5/5] Updating monitor state...")
    save_previous_data(new_data, prev_data_path)
    
    # Summary
    print("\n" + "=" * 60)
    print("UPDATE CHECK SUMMARY:")
    print(f"  New Notifications: {len(updates['new_notifications'])}")
    print(f"  New PYQ Papers: {len(updates['new_pyqs'])}")
    print(f"  New Syllabus PDFs: {len(updates['new_syllabus'])}")
    print("=" * 60)
    
    return updates


if __name__ == "__main__":
    generate_update_alerts()

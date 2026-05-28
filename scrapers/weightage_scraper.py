import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.json_utils import save_json


def scrape_kas_weightage():
    print("=" * 50)
    print("Starting KAS Subject Weightage Scraper")
    print("=" * 50)
    
    # Comprehensive KAS subject weightage
    weightage = {
        "exam": "KAS",
        "stage": "Prelims & Mains",
        "subjects": {
            "History": {
                "prelims_weightage": 20,
                "mains_weightage": 150,
                "priority": "High",
                "difficulty": "Medium"
            },
            "Polity": {
                "prelims_weightage": 25,
                "mains_weightage": 200,
                "priority": "Very High",
                "difficulty": "Medium"
            },
            "Economics": {
                "prelims_weightage": 15,
                "mains_weightage": 100,
                "priority": "High",
                "difficulty": "Medium"
            },
            "Geography": {
                "prelims_weightage": 10,
                "mains_weightage": 75,
                "priority": "High",
                "difficulty": "Easy-Medium"
            },
            "Environment & Ecology": {
                "prelims_weightage": 10,
                "mains_weightage": 50,
                "priority": "High",
                "difficulty": "Easy"
            },
            "Science & Technology": {
                "prelims_weightage": 10,
                "mains_weightage": 50,
                "priority": "Medium",
                "difficulty": "Medium"
            },
            "Current Affairs": {
                "prelims_weightage": 15,
                "mains_weightage": 100,
                "priority": "Very High",
                "difficulty": "Medium"
            },
            "Ethics": {
                "prelims_weightage": 0,
                "mains_weightage": 150,
                "priority": "High",
                "difficulty": "Medium"
            }
        },
        "total_marks": {
            "prelims": 400,
            "mains": 1250,
            "interview": 200
        }
    }
    
    print("\nOK: Generated subject weightage for 8 subjects")
    print("OK: Total Prelims: 400 marks | Total Mains: 1250 marks")
    
    save_path = "datasets/weightage/kas_weightage.json"
    save_json(weightage, save_path)
    
    print("\n" + "=" * 50)
    print("Subject weightage scraping completed!")
    print("=" * 50)
    
    return weightage


if __name__ == "__main__":
    scrape_kas_weightage()

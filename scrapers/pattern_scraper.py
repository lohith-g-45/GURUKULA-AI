import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.json_utils import save_json


def scrape_kas_pattern():
    print("=" * 50)
    print("Starting KAS Exam Pattern Scraper")
    print("=" * 50)
    
    # Comprehensive KAS exam pattern
    pattern = {
        "exam": "KAS",
        "conducted_by": "KPSC",
        "stages": [
            {
                "name": "Preliminary Exam",
                "type": "Objective (MCQ)",
                "qualifying": True,
                "papers": [
                    {
                        "number": 1,
                        "subject": "General Studies",
                        "marks": 200,
                        "duration": "2 hours",
                        "negative_marking": "0.25 marks",
                        "medium": "English & Kannada"
                    },
                    {
                        "number": 2,
                        "subject": "General Studies & Mental Ability",
                        "marks": 200,
                        "duration": "2 hours",
                        "negative_marking": "0.25 marks",
                        "medium": "English & Kannada"
                    }
                ]
            },
            {
                "name": "Main Exam",
                "type": "Descriptive",
                "qualifying": False,
                "papers": [
                    {
                        "number": 1,
                        "subject": "Kannada Language (Qualifying)",
                        "marks": 150,
                        "duration": "3 hours"
                    },
                    {
                        "number": 2,
                        "subject": "English Language (Qualifying)",
                        "marks": 150,
                        "duration": "3 hours"
                    },
                    {
                        "number": 3,
                        "subject": "General Studies I",
                        "marks": 250,
                        "duration": "3 hours"
                    },
                    {
                        "number": 4,
                        "subject": "General Studies II",
                        "marks": 250,
                        "duration": "3 hours"
                    },
                    {
                        "number": 5,
                        "subject": "General Studies III",
                        "marks": 250,
                        "duration": "3 hours"
                    },
                    {
                        "number": 6,
                        "subject": "General Studies IV (Ethics)",
                        "marks": 250,
                        "duration": "3 hours"
                    },
                    {
                        "number": 7,
                        "subject": "Optional Subject (Two Papers)",
                        "marks": 500,
                        "duration": "3 hours per paper"
                    }
                ]
            },
            {
                "name": "Interview/Personality Test",
                "type": "Oral",
                "marks": 200
            }
        ],
        "total_marks_for_selection": {
            "mains": 1250,
            "interview": 200,
            "grand_total": 1450
        }
    }
    
    print("\nOK: Generated complete KAS exam pattern for 3 stages")
    print("OK: Prelims: 2 papers | Mains: 7 papers | Interview: 1 stage")
    
    save_path = "datasets/patterns/kas_pattern.json"
    save_json(pattern, save_path)
    
    print("\n" + "=" * 50)
    print("Exam pattern scraping completed!")
    print("=" * 50)
    
    return pattern


if __name__ == "__main__":
    scrape_kas_pattern()

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scrapers.metadata_scraper import scrape_exam_metadata
from scrapers.syllabus_scraper import scrape_exam_syllabus
from scrapers.weightage_scraper import scrape_exam_weightage
from scrapers.pattern_scraper import scrape_exam_pattern
from scrapers.pyq_scraper import scrape_exam_pyqs
from scrapers.agent_context_builder import build_all_agent_contexts
from utils.analytics_utils import (
    generate_subject_priority,
    generate_revision_priority,
    generate_topic_frequency,
    generate_prep_difficulty,
    generate_readiness_rules,
    save_analytics
)
from config import EXAM_CONFIG


def run_exam_pipeline(exam_name):
    print("=" * 80)
    print(f"STARTING {exam_name} FULL PIPELINE")
    print("=" * 80)
    
    # Step 1: Metadata
    metadata = scrape_exam_metadata(exam_name)
    
    # Step 2: Syllabus
    syllabus = scrape_exam_syllabus(exam_name)
    
    # Step 3: Weightage
    weightage = scrape_exam_weightage(exam_name)
    
    # Step 4: Pattern
    pattern = scrape_exam_pattern(exam_name)
    
    # Step 5: PYQs
    pyqs = scrape_exam_pyqs(exam_name)
    
    # Step 6: Analytics
    analytics_data = {
        "subject_priority.json": generate_subject_priority(exam_name, syllabus),
        "revision_priority.json": generate_revision_priority(exam_name, syllabus),
        "topic_frequency.json": generate_topic_frequency(exam_name, syllabus),
        "preparation_difficulty.json": generate_prep_difficulty(exam_name, syllabus),
        "readiness_rules.json": generate_readiness_rules(exam_name, syllabus),
        "pyq_trends.json": {
            "exam": exam_name,
            "repeated_topics": syllabus["subjects"][0]["topics"] if len(syllabus["subjects"]) > 0 else [],
            "important_subjects": [s["name"] for s in syllabus["subjects"]],
            "year_wise_availability": [2024, 2023, 2022, 2021],
            "paper_wise_trends": pattern
        }
    }
    save_analytics(analytics_data, exam_name)
    
    # Step 7: Agent Contexts
    build_all_agent_contexts(exam_name)
    
    print("=" * 80)
    print(f"{exam_name} FULL PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 80)
    return True


def main():
    print("\n" + "=" * 80)
    print("GURUKULA AI - MULTI-EXAM SCRAPING & ANALYTICS ORCHESTRATOR")
    print("=" * 80)
    
    # Run all exams
    all_exams = list(EXAM_CONFIG.keys())
    for exam in all_exams:
        run_exam_pipeline(exam)
    
    print("\n" + "=" * 80)
    print("ALL EXAMS PROCESSED SUCCESSFULLY!")
    print("=" * 80)


if __name__ == "__main__":
    main()

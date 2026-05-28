from scrapers.metadata_scraper import scrape_kas_metadata
from scrapers.syllabus_scraper import scrape_kas_syllabus
from scrapers.weightage_scraper import scrape_kas_weightage
from scrapers.pattern_scraper import scrape_kas_pattern
from scrapers.pyq_scraper import scrape_kas_pyqs
from scrapers.update_checker import generate_update_alerts
from scrapers.agent_context_builder import main as build_agent_contexts
from utils.analytics_utils import (
    generate_subject_priority, 
    generate_revision_priority, 
    generate_topic_frequency, 
    generate_prep_difficulty, 
    generate_readiness_rules,
    save_analytics
)
from utils.json_utils import load_json


def main():
    print("=" * 80)
    print("GURUKULA AI - ADVANCED INTELLIGENCE ENGINE")
    print("=" * 80)
    
    print("\n[0/9] Checking for KPSC updates...")
    updates = generate_update_alerts()
    
    print("\n[1/9] Scraping KAS Metadata...")
    metadata = scrape_kas_metadata()
    
    print("\n[2/9] Scraping KAS Syllabus...")
    syllabus = scrape_kas_syllabus()
    
    print("\n[3/9] Scraping KAS Subject Weightage...")
    weightage = scrape_kas_weightage()
    
    print("\n[4/9] Scraping KAS Exam Pattern...")
    pattern = scrape_kas_pattern()
    
    print("\n[5/9] Scraping KAS Previous Year Question Papers...")
    pyq_data = scrape_kas_pyqs()
    
    print("\n[6/9] Generating AI-Ready Analytics...")
    analytics = {
        "subject_priority.json": generate_subject_priority(syllabus),
        "revision_priority.json": generate_revision_priority(syllabus),
        "topic_frequency.json": generate_topic_frequency(syllabus),
        "preparation_difficulty.json": generate_prep_difficulty(syllabus),
        "readiness_rules.json": generate_readiness_rules(syllabus)
    }
    save_analytics(analytics, "datasets/analytics")
    print("OK: All analytics datasets generated successfully!")
    
    print("\n[7/9] Building AI Agent Contexts...")
    build_agent_contexts()
    
    print("\n[8/9] Finalizing Intelligence Engine...")
    print("=" * 80)
    print("GURUKULA AI INTELLIGENCE ENGINE RUN COMPLETED SUCCESSFULLY!")
    print("All datasets and agent contexts are AI-Ready!")
    print("Check datasets/ directory for all files!")
    print("=" * 80)


if __name__ == "__main__":
    main()

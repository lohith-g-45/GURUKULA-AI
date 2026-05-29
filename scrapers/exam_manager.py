import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.pyq_analyzer import generate_kas_analytics
from scrapers.agent_context_builder import build_all_agent_contexts
from config import EXAM_CONFIG


def run_exam_pipeline(exam_name: str) -> bool:
    print("\n" + "=" * 80)
    print(f"STARTING {exam_name} FULL INTELLIGENCE PIPELINE")
    print("=" * 80)
    
    if exam_name == "KAS":
        print("\n[Step 1] Generating REAL KAS analytics from PYQs...")
        analytics_success = generate_kas_analytics(exam_name)
        
        if not analytics_success:
            print("\n❌ Analytics generation failed!")
            return False
        
        print("\n[Step 2] Building agent contexts...")
        build_all_agent_contexts(exam_name)
        
        print("\n" + "=" * 80)
        print(f"✅ {exam_name} PIPELINE COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        return True
    else:
        print(f"\n⚠️ Pipeline for {exam_name} not fully implemented yet")
        return False


def main():
    print("\n" + "=" * 80)
    print("GURUKULA AI - INTELLIGENCE PIPELINE ORCHESTRATOR")
    print("=" * 80)
    
    for exam_name in EXAM_CONFIG.keys():
        if exam_name == "KAS":
            run_exam_pipeline(exam_name)
    
    print("\n" + "=" * 80)
    print("ALL PROCESSING COMPLETE!")
    print("=" * 80)


if __name__ == "__main__":
    main()


import os
import json

def quick_check():
    print("="*60)
    print("GURUKULA AI - Quick Validation Check")
    print("="*60)
    
    root_dir = os.path.join(os.path.dirname(__file__), "datasets", "KAS")
    
    # 1. Check directories exist
    print("\n[1] Checking directory structure...")
    required_dirs = [
        "agent_contexts", "analytics", "exams", "intelligence",
        "patterns", "planning", "prompts", "pyqs", "raw",
        "recommendations", "syllabus", "weightage"
    ]
    all_dirs_ok = True
    for d in required_dirs:
        dir_path = os.path.join(root_dir, d)
        if os.path.exists(dir_path):
            print(f"  [OK] {d}/ exists")
        else:
            print(f"  [ERROR] {d}/ missing")
            all_dirs_ok = False
    
    # 2. Check key files exist
    print("\n[2] Checking key files exist...")
    key_files = [
        "analytics/kas_pyq_metadata.json",
        "analytics/kas_subject_weightage.json",
        "intelligence/readiness_rules.json",
        "recommendations/recommendation_engine.json",
        "planning/roadmap_rules.json",
        "prompts/insight_prompt.txt",
        "prompts/planning_prompt.txt",
        "prompts/research_prompt.txt",
        "prompts/revision_prompt.txt",
        "syllabus/kas_syllabus.json"
    ]
    all_files_ok = True
    for f in key_files:
        file_path = os.path.join(root_dir, f)
        if os.path.exists(file_path):
            print(f"  [OK] {f} exists")
        else:
            print(f"  [ERROR] {f} missing")
            all_files_ok = False
    
    # 3. Check subject weightage consistency
    print("\n[3] Checking subject weightage consistency...")
    weightage_files = [
        os.path.join(root_dir, "analytics", "kas_subject_weightage.json"),
        os.path.join(root_dir, "weightage", "kas_weightage.json")
    ]
    
    weightage_data = []
    for f in weightage_files:
        with open(f, 'r', encoding='utf-8') as fp:
            data = json.load(fp)
            if 'subjects' in data:
                weightage_data.append(data['subjects'])
            elif 'subject_weightage' in data:
                weightage_data.append(data['subject_weightage'])
    
    consistent = True
    if len(weightage_data) > 1:
        for subject in weightage_data[0]:
            if subject not in weightage_data[1]:
                print(f"  [ERROR] Subject {subject} missing in one file")
                consistent = False
            else:
                # Check prelims weightage matches
                w1 = weightage_data[0][subject].get('prelims_weightage')
                w2 = weightage_data[1][subject].get('prelims_weightage')
                if w1 != w2:
                    print(f"  [ERROR] Mismatch for {subject} prelims weightage: {w1} vs {w2}")
                    consistent = False
    if consistent:
        print("  [OK] Subject weightages are consistent")
    
    # Summary
    print("\n" + "="*60)
    if all_dirs_ok and all_files_ok and consistent:
        print("[SUCCESS] Quick check passed!")
    else:
        print("[FAILURE] Some issues found! Please check above.")
    print("="*60)

if __name__ == "__main__":
    quick_check()


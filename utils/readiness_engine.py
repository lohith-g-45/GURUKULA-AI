import os
import sys
import math
from typing import Dict, List, Any, Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.json_utils import save_json, load_json
from utils.dataset_manager import get_data_path


def calculate_diminishing_returns(value: float, max_value: float) -> float:
    """Apply diminishing returns to prevent easy 100% scores"""
    if value <= 0:
        return 0
    return max_value * (1 - math.exp(-value / (max_value / 2)))


def calculate_subject_priority_weight(subject: str, subject_weightage: Dict[str, Dict]) -> float:
    """Calculate priority weight for a subject based on real analytics"""
    if subject not in subject_weightage:
        return 1.0
    
    data = subject_weightage[subject]
    total_weight = data["prelims_weightage"] + data["mains_weightage"]
    priority_multiplier = {
        "Very High": 2.0,
        "High": 1.5,
        "Medium": 1.0
    }
    return (total_weight / 20) * priority_multiplier.get(data["priority"], 1.0)


def calculate_readiness_score(
    daily_study_hours: float,
    weak_subjects: List[str],
    strong_subjects: List[str],
    preparation_level: float,  # 0-100
    exam_date_proximity: int,  # days left
    consistency_level: float,  # 0-100
    subject_weightage: Dict[str, Dict]
) -> Dict[str, Any]:
    """Calculate comprehensive readiness score with advanced logic"""

    # 1. Calculate study efficiency (consistency * hours)
    study_efficiency = (consistency_level / 100) * (daily_study_hours / 8)  # Normalize to 8 hours as max

    # 2. Base score from preparation level with diminishing returns
    base_score = calculate_diminishing_returns(preparation_level, 100)

    # 3. Study hours impact with diminishing returns
    if daily_study_hours >= 10:
        study_base = 12
    elif daily_study_hours >= 8:
        study_base = 10
    elif daily_study_hours >= 6:
        study_base = 7
    elif daily_study_hours >= 4:
        study_base = 4
    elif daily_study_hours >= 2:
        study_base = 1
    else:
        study_base = -5
    
    study_bonus = study_base * study_efficiency

    # 4. Consistency impact with diminishing returns
    consistency_bonus = calculate_diminishing_returns((consistency_level / 100) * 15, 15)

    # 5. Strong subjects impact (weighted by priority)
    strong_subject_bonus = 0
    for subject in strong_subjects:
        weight = calculate_subject_priority_weight(subject, subject_weightage)
        strong_subject_bonus += weight * 2

    strong_subject_bonus = calculate_diminishing_returns(strong_subject_bonus, 20)

    # 6. Weak subjects impact (weighted by priority, amplified near exam)
    weak_subject_penalty = 0
    exam_proximity_multiplier = 1.0
    if exam_date_proximity <= 7:
        exam_proximity_multiplier = 2.0
    elif exam_date_proximity <= 30:
        exam_proximity_multiplier = 1.5
    elif exam_date_proximity <= 90:
        exam_proximity_multiplier = 1.2

    for subject in weak_subjects:
        weight = calculate_subject_priority_weight(subject, subject_weightage)
        weak_subject_penalty += weight * 3 * exam_proximity_multiplier

    weak_subject_penalty = min(weak_subject_penalty, 40)

    # 7. Calculate prelims and mains readiness separately
    prelims_raw = base_score
    mains_raw = base_score

    for subject in strong_subjects:
        if subject in subject_weightage:
            prelims_raw += subject_weightage[subject]["prelims_weightage"] / 10
            mains_raw += subject_weightage[subject]["mains_weightage"] / 10

    for subject in weak_subjects:
        if subject in subject_weightage:
            prelims_raw -= subject_weightage[subject]["prelims_weightage"] / 8 * exam_proximity_multiplier
            mains_raw -= subject_weightage[subject]["mains_weightage"] / 8 * exam_proximity_multiplier

    prelims_raw += study_bonus + consistency_bonus
    mains_raw += study_bonus + consistency_bonus

    prelims_readiness = max(0, min(100, calculate_diminishing_returns(prelims_raw, 100)))
    mains_readiness = max(0, min(100, calculate_diminishing_returns(mains_raw, 100)))

    # 8. Overall readiness
    raw_overall = (prelims_readiness + mains_readiness) / 2
    readiness_score = max(0, min(100, raw_overall))

    # 9. Advanced risk calculation (multi-factor)
    risk_factors = []
    
    # Factor 1: Readiness score
    if readiness_score < 50:
        risk_factors.append(30)
    elif readiness_score < 65:
        risk_factors.append(20)
    elif readiness_score < 80:
        risk_factors.append(10)
    else:
        risk_factors.append(0)
    
    # Factor 2: Consistency
    if consistency_level < 40:
        risk_factors.append(25)
    elif consistency_level < 60:
        risk_factors.append(15)
    elif consistency_level < 80:
        risk_factors.append(5)
    else:
        risk_factors.append(0)
    
    # Factor 3: Exam proximity
    if exam_date_proximity <= 7 and readiness_score < 70:
        risk_factors.append(20)
    elif exam_date_proximity <= 30 and readiness_score < 60:
        risk_factors.append(15)
    else:
        risk_factors.append(0)
    
    # Factor 4: Weak subject count (especially high-priority)
    high_priority_weak = [s for s in weak_subjects if s in subject_weightage and subject_weightage[s]["priority"] in ["Very High", "High"]]
    if len(high_priority_weak) >= 3:
        risk_factors.append(25)
    elif len(high_priority_weak) >= 2:
        risk_factors.append(15)
    elif len(high_priority_weak) >= 1:
        risk_factors.append(5)
    else:
        risk_factors.append(0)
    
    # Factor 5: Burnout indicator (long hours + low consistency)
    if daily_study_hours >= 8 and consistency_level < 50:
        risk_factors.append(15)
    elif daily_study_hours >= 10 and consistency_level < 60:
        risk_factors.append(20)
    else:
        risk_factors.append(0)
    
    total_risk_score = sum(risk_factors)
    
    if total_risk_score <= 10:
        risk = "Low"
    elif total_risk_score <= 30:
        risk = "Medium"
    elif total_risk_score <= 50:
        risk = "High"
    else:
        risk = "Critical"

    return {
        "readiness": round(readiness_score, 1),
        "prelims_readiness": round(prelims_readiness, 1),
        "mains_readiness": round(mains_readiness, 1),
        "risk": risk,
        "risk_score": round(total_risk_score, 1),
        "consistency": round(consistency_level, 1),
        "study_efficiency": round(study_efficiency * 100, 1),
        "breakdown": {
            "base_preparation": round(base_score, 1),
            "study_hours_impact": round(study_bonus, 1),
            "consistency_impact": round(consistency_bonus, 1),
            "strong_subjects_impact": round(strong_subject_bonus, 1),
            "weak_subjects_impact": round(-weak_subject_penalty, 1),
            "exam_proximity_multiplier": exam_proximity_multiplier
        }
    }


def generate_readiness_rules() -> Dict[str, Any]:
    """Generate advanced readiness rules configuration"""
    return {
        "version": "2.0",
        "rules": {
            "study_hours": {
                "excellent": {"min_hours": 10, "bonus": 12, "description": "10+ hours daily - excellent"},
                "very_good": {"min_hours": 8, "bonus": 10, "description": "8-10 hours daily - very good"},
                "good": {"min_hours": 6, "bonus": 7, "description": "6-8 hours daily - good"},
                "average": {"min_hours": 4, "bonus": 4, "description": "4-6 hours daily - average"},
                "low": {"min_hours": 2, "bonus": 1, "description": "2-4 hours daily - low"},
                "very_low": {"min_hours": 0, "bonus": -5, "description": "Less than 2 hours daily - very low"}
            },
            "consistency": {
                "scaling_factor": 0.15,
                "max_impact": 15,
                "diminishing_returns": True,
                "description": "Consistency contributes up to 15 points with diminishing returns"
            },
            "subject_impact": {
                "strong_subject_scaling": 0.1,
                "weak_subject_scaling": 0.15,
                "priority_weighting": True,
                "description": "Strong/weak subjects weighted by real subject priority from analytics"
            },
            "exam_proximity": {
                "critical": {"max_days": 7, "weak_penalty_multiplier": 2.0, "description": "Less than 1 week - very high pressure"},
                "near": {"max_days": 30, "weak_penalty_multiplier": 1.5, "description": "Less than 1 month - high pressure"},
                "medium": {"max_days": 90, "weak_penalty_multiplier": 1.2, "description": "1-3 months - moderate pressure"},
                "far": {"max_days": 365, "weak_penalty_multiplier": 1.0, "description": "More than 3 months - low pressure"}
            },
            "study_efficiency": {
                "calculation": "(consistency_level / 100) * (daily_study_hours / 8)",
                "description": "Study efficiency = consistency * normalized study hours"
            }
        }
    }


def generate_scoring_formulas() -> Dict[str, Any]:
    """Generate advanced scoring formulas documentation"""
    return {
        "version": "2.0",
        "formulas": {
            "diminishing_returns": "max_value * (1 - exp(-value / (max_value / 2)))",
            "readiness_score": "max(0, min(100, (prelims_readiness + mains_readiness) / 2))",
            "prelims_readiness": "diminishing_returns(base + study_bonus + consistency_bonus + strong_prelims_bonus - weak_prelims_penalty, 100)",
            "mains_readiness": "diminishing_returns(base + study_bonus + consistency_bonus + strong_mains_bonus - weak_mains_penalty, 100)",
            "study_efficiency": "(consistency_level / 100) * (daily_study_hours / 8)",
            "subject_priority_weight": "(total_weight / 20) * priority_multiplier"
        },
        "parameters": {
            "daily_study_hours": "float - Average daily study time in hours",
            "weak_subjects": "List[str] - Subjects student finds difficult",
            "strong_subjects": "List[str] - Subjects student is confident in",
            "preparation_level": "float (0-100) - Self-assessed preparation level",
            "exam_date_proximity": "int - Days remaining until exam",
            "consistency_level": "float (0-100) - How consistent student is with studies"
        },
        "outputs": {
            "readiness": "float (0-100) - Overall readiness score",
            "prelims_readiness": "float (0-100) - Prelims-specific readiness",
            "mains_readiness": "float (0-100) - Mains-specific readiness",
            "risk": "str - Low/Medium/High/Critical risk level",
            "risk_score": "float - Numeric risk score for detailed analysis",
            "consistency": "float (0-100) - Consistency score",
            "study_efficiency": "float (0-100) - Study efficiency score"
        }
    }


def generate_consistency_rules() -> Dict[str, Any]:
    """Generate consistency scoring rules"""
    return {
        "version": "2.0",
        "rules": {
            "daily_streak": {
                "30+ days": {"score": 100, "description": "Excellent consistency"},
                "15-29 days": {"score": 85, "description": "Very good consistency"},
                "7-14 days": {"score": 70, "description": "Good consistency"},
                "3-6 days": {"score": 50, "description": "Average consistency"},
                "1-2 days": {"score": 30, "description": "Low consistency"},
                "0 days": {"score": 0, "description": "No consistency"}
            },
            "weekly_study_days": {
                "7 days": {"bonus": 10, "description": "Studies every day"},
                "5-6 days": {"bonus": 5, "description": "Studies most days"},
                "3-4 days": {"bonus": 0, "description": "Studies some days"},
                "1-2 days": {"bonus": -5, "description": "Studies rarely"},
                "0 days": {"bonus": -10, "description": "No study"}
            }
        },
        "calculation": "consistency_score = (streak_score + weekly_bonus) * 0.5"
    }


def generate_risk_rules() -> Dict[str, Any]:
    """Generate risk rules configuration"""
    return {
        "version": "1.0",
        "risk_factors": {
            "readiness_score": {
                "weight": 30,
                "levels": {
                    "<50": 30,
                    "50-65": 20,
                    "65-80": 10,
                    ">=80": 0
                }
            },
            "consistency": {
                "weight": 25,
                "levels": {
                    "<40": 25,
                    "40-60": 15,
                    "60-80": 5,
                    ">=80": 0
                }
            },
            "exam_proximity": {
                "weight": 20,
                "conditions": {
                    "<=7 days & readiness<70": 20,
                    "<=30 days & readiness<60": 15,
                    "default": 0
                }
            },
            "weak_high_priority_subjects": {
                "weight": 25,
                "levels": {
                    ">=3": 25,
                    ">=2": 15,
                    ">=1": 5,
                    "0": 0
                }
            },
            "burnout_indicator": {
                "weight": 20,
                "conditions": {
                    ">=10 hours & consistency<60": 20,
                    ">=8 hours & consistency<50": 15,
                    "default": 0
                }
            }
        },
        "risk_levels": {
            "Low": {"max_score": 10, "description": "Very low risk - well prepared"},
            "Medium": {"max_score": 30, "description": "Moderate risk - some improvements needed"},
            "High": {"max_score": 50, "description": "High risk - significant improvements needed"},
            "Critical": {"max_score": 100, "description": "Critical risk - immediate action required"}
        }
    }


def generate_phase2_intelligence(exam_name: str = "KAS") -> bool:
    """Generate Phase 2 intelligence files with advanced refinement"""
    print("\n" + "=" * 80)
    print("GURUKULA AI - READINESS INTELLIGENCE ENGINE")
    print("PHASE 2: ADVANCED READINESS SCORING REFINEMENT")
    print("=" * 80)

    analytics_dir = get_data_path(exam_name, "analytics")
    intelligence_dir = get_data_path(exam_name, "intelligence")

    # Load analytics data
    print(f"\n[1/8] Loading analytics data from {analytics_dir}...")
    subject_weightage = load_json(os.path.join(analytics_dir, "kas_subject_weightage.json"))["subjects"]

    print(f"\n[2/8] Generating readiness rules (v2.0)...")
    readiness_rules = generate_readiness_rules()

    print(f"\n[3/8] Generating scoring formulas (v2.0)...")
    scoring_formulas = generate_scoring_formulas()

    print(f"\n[4/8] Generating consistency rules (v2.0)...")
    consistency_rules = generate_consistency_rules()

    print(f"\n[5/8] Generating risk rules...")
    risk_rules = generate_risk_rules()

    print(f"\n[6/8] Saving intelligence files to {intelligence_dir}...")
    save_json(readiness_rules, os.path.join(intelligence_dir, "readiness_rules.json"))
    save_json(scoring_formulas, os.path.join(intelligence_dir, "scoring_formulas.json"))
    save_json(consistency_rules, os.path.join(intelligence_dir, "consistency_rules.json"))
    save_json(risk_rules, os.path.join(intelligence_dir, "risk_rules.json"))

    print(f"\n[7/8] Generating sample readiness outputs...")
    # Generate sample outputs for different student types
    sample_students = [
        {
            "name": "Weak Student",
            "profile": {
                "daily_study_hours": 2,
                "weak_subjects": ["History", "Polity", "Geography", "Economics", "Environment"],
                "strong_subjects": [],
                "preparation_level": 30,
                "exam_date_proximity": 30,
                "consistency_level": 25
            }
        },
        {
            "name": "Average Student",
            "profile": {
                "daily_study_hours": 5,
                "weak_subjects": ["History", "Environment"],
                "strong_subjects": ["Science & Technology", "Current Affairs"],
                "preparation_level": 60,
                "exam_date_proximity": 45,
                "consistency_level": 65
            }
        },
        {
            "name": "Strong Student",
            "profile": {
                "daily_study_hours": 8,
                "weak_subjects": ["Environment"],
                "strong_subjects": ["Polity", "Science & Technology", "Current Affairs", "Karnataka GK"],
                "preparation_level": 85,
                "exam_date_proximity": 60,
                "consistency_level": 90
            }
        },
        {
            "name": "Burnout-Risk Student",
            "profile": {
                "daily_study_hours": 12,
                "weak_subjects": ["Polity", "Economics", "Geography"],
                "strong_subjects": ["Science & Technology", "CSAT"],
                "preparation_level": 75,
                "exam_date_proximity": 10,
                "consistency_level": 45
            }
        },
        {
            "name": "Exceptional Student",
            "profile": {
                "daily_study_hours": 10,
                "weak_subjects": [],
                "strong_subjects": ["History", "Polity", "Geography", "Economics", "Environment", "Science & Technology", "Karnataka GK", "Current Affairs", "CSAT"],
                "preparation_level": 98,
                "exam_date_proximity": 14,
                "consistency_level": 98
            }
        }
    ]

    print("\n" + "=" * 80)
    print("SAMPLE STUDENT READINESS OUTPUTS")
    print("=" * 80)

    for student in sample_students:
        result = calculate_readiness_score(
            student["profile"]["daily_study_hours"],
            student["profile"]["weak_subjects"],
            student["profile"]["strong_subjects"],
            student["profile"]["preparation_level"],
            student["profile"]["exam_date_proximity"],
            student["profile"]["consistency_level"],
            subject_weightage
        )
        print(f"\n  {student['name']}:")
        print(f"    Overall Readiness: {result['readiness']}%")
        print(f"    Prelims Readiness: {result['prelims_readiness']}%")
        print(f"    Mains Readiness: {result['mains_readiness']}%")
        print(f"    Risk Level: {result['risk']} (Score: {result['risk_score']})")
        print(f"    Consistency: {result['consistency']}%")
        print(f"    Study Efficiency: {result['study_efficiency']}%")

    # Validate all JSON files are valid
    print("\n" + "=" * 80)
    print("VALIDATION REPORT")
    print("=" * 80)
    try:
        load_json(os.path.join(intelligence_dir, "readiness_rules.json"))
        load_json(os.path.join(intelligence_dir, "scoring_formulas.json"))
        load_json(os.path.join(intelligence_dir, "consistency_rules.json"))
        load_json(os.path.join(intelligence_dir, "risk_rules.json"))
        print("\n  [OK] All JSON files are valid!")
    except Exception as e:
        print(f"\n  [ERROR] JSON validation failed: {e}")
        return False

    # Verify readiness doesn't easily reach 100
    print("\n  Readiness Distribution Check:")
    all_samples_valid = True
    for student in sample_students:
        result = calculate_readiness_score(
            student["profile"]["daily_study_hours"],
            student["profile"]["weak_subjects"],
            student["profile"]["strong_subjects"],
            student["profile"]["preparation_level"],
            student["profile"]["exam_date_proximity"],
            student["profile"]["consistency_level"],
            subject_weightage
        )
        if student["name"] != "Exceptional Student" and result["readiness"] >= 95:
            all_samples_valid = False
            print(f"    [WARNING] {student['name']} has readiness {result['readiness']}% (should be <95%)")
        else:
            print(f"    [OK] {student['name']} readiness is reasonable: {result['readiness']}%")

    print("\n" + "=" * 80)
    print("PHASE 2 REFINEMENT COMPLETE!")
    print("=" * 80)
    print("\nFiles Generated/Updated:")
    print("  - readiness_rules.json (v2.0)")
    print("  - scoring_formulas.json (v2.0)")
    print("  - consistency_rules.json (v2.0)")
    print("  - risk_rules.json (new)")
    print("\nKey Improvements:")
    print("  - Diminishing returns to prevent easy 100% scores")
    print("  - Subject priority weighting using real analytics")
    print("  - Advanced multi-factor risk calculation")
    print("  - Exam proximity scaling for weak subjects")
    print("  - Study efficiency logic")
    print("  - Separate prelims/mains readiness scores")
    print("  - Critical risk level added")
    print("  - Burnout indicator")

    return all_samples_valid


if __name__ == "__main__":
    generate_phase2_intelligence("KAS")

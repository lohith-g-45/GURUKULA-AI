import os


def generate_subject_priority(syllabus_data):
    """Generate subject priority scores based on weightage, difficulty, and importance"""
    subjects = syllabus_data.get('subjects', [])
    priority_scores = []
    
    for subject in subjects:
        weightage = subject.get('estimated_weightage', 10)
        difficulty_score = {"Easy": 1, "Easy-Medium": 2, "Medium": 3, "Hard": 4}.get(
            subject.get('difficulty', "Medium"), 3
        )
        priority_score = weightage * (5 - difficulty_score)
        
        priority_scores.append({
            "subject": subject.get('name'),
            "priority_score": priority_score,
            "estimated_weightage": weightage,
            "difficulty": subject.get('difficulty'),
            "preparation_complexity": subject.get('preparation_complexity', "Medium"),
            "revision_frequency": subject.get('revision_frequency', "Weekly"),
            "recommended_revision_gap": subject.get('recommended_revision_gap', "3-5 days"),
            "weak_area_focus": subject.get('weak_area_focus', "High")
        })
    
    priority_scores.sort(key=lambda x: x['priority_score'], reverse=True)
    return priority_scores


def generate_revision_priority(syllabus_data):
    """Generate revision priority for each topic"""
    revision_priority = []
    
    for subject in syllabus_data.get('subjects', []):
        for topic in subject.get('topics', []):
            revision_priority.append({
                "subject": subject.get('name'),
                "topic": topic.get('name'),
                "importance": topic.get('importance', "Medium"),
                "pyq_frequency": topic.get('pyq_frequency', "Medium"),
                "revision_priority": topic.get('revision_priority', "Medium"),
                "estimated_prep_time": topic.get('estimated_prep_time', "2-3 hours"),
                "weak_topic_sensitivity": topic.get('weak_topic_sensitivity', "Medium")
            })
    
    # Sort by importance and pyq frequency
    priority_order = {"Very High": 4, "High": 3, "Medium": 2, "Low": 1}
    revision_priority.sort(
        key=lambda x: (
            priority_order.get(x['importance'], 2), 
            priority_order.get(x['pyq_frequency'], 2)
        ), 
        reverse=True
    )
    
    return revision_priority


def generate_topic_frequency(syllabus_data):
    """Generate topic frequency data"""
    topic_frequency = []
    
    for subject in syllabus_data.get('subjects', []):
        for topic in subject.get('topics', []):
            freq_score = {"Very High": 10, "High": 7, "Medium": 4, "Low": 2}.get(
                topic.get('pyq_frequency', "Medium"), 4
            )
            topic_frequency.append({
                "subject": subject.get('name'),
                "topic": topic.get('name'),
                "frequency_score": freq_score,
                "importance": topic.get('importance', "Medium")
            })
    
    topic_frequency.sort(key=lambda x: x['frequency_score'], reverse=True)
    return topic_frequency


def generate_prep_difficulty(syllabus_data):
    """Generate preparation difficulty analysis"""
    categories = {
        "easy_subjects": [],
        "medium_subjects": [],
        "hard_subjects": [],
        "time_consuming_subjects": []
    }
    
    for subject in syllabus_data.get('subjects', []):
        name = subject.get('name')
        difficulty = subject.get('difficulty', "Medium")
        complexity = subject.get('preparation_complexity', "Medium")
        
        if difficulty in ["Easy", "Easy-Medium"]:
            categories["easy_subjects"].append(name)
        elif difficulty == "Medium":
            categories["medium_subjects"].append(name)
        else:
            categories["hard_subjects"].append(name)
            
        if complexity in ["High", "Very High"]:
            categories["time_consuming_subjects"].append(name)
    
    return categories


def generate_readiness_rules(syllabus_data):
    """Generate readiness rules for AI agents"""
    return {
        "research_agent": {
            "focus_areas": ["High priority subjects", "High PYQ frequency topics"],
            "data_needed": ["syllabus", "pyqs", "weightage"]
        },
        "planning_agent": {
            "focus_areas": ["Subject prioritization", "Time allocation"],
            "data_needed": ["subject_priority", "prep_difficulty"]
        },
        "revision_agent": {
            "focus_areas": ["Revision scheduling", "Weak areas"],
            "data_needed": ["revision_priority", "topic_frequency"]
        },
        "insight_agent": {
            "focus_areas": ["Trend analysis", "Pattern recognition"],
            "data_needed": ["topic_frequency", "pyq_trends"]
        },
        "trend_analysis_agent": {
            "focus_areas": ["Year-wise trends", "Paper-wise trends"],
            "data_needed": ["topic_frequency", "pyq_trends"]
        }
    }


def generate_pyq_trends(pyq_data):
    """Generate PYQ trends analysis"""
    trends = {
        "repeated_topic_frequency": {},
        "important_subjects": [],
        "year_wise_trends": {},
        "paper_wise_trends": {},
        "high_frequency_topics": []
    }
    
    for paper in pyq_data.get('papers', []):
        year = paper.get('year')
        stage = paper.get('stage')
        paper_num = paper.get('paper')
        
        if year not in trends['year_wise_trends']:
            trends['year_wise_trends'][year] = []
        trends['year_wise_trends'][year].append({
            "stage": stage,
            "paper": paper_num,
            "title": paper.get('title')
        })
        
        paper_key = f"{stage}_{paper_num}"
        if paper_key not in trends['paper_wise_trends']:
            trends['paper_wise_trends'][paper_key] = []
        trends['paper_wise_trends'][paper_key].append(year)
    
    return trends


def save_analytics(analytics_data, base_dir="datasets/analytics"):
    """Save all analytics files to disk"""
    os.makedirs(base_dir, exist_ok=True)
    from utils.json_utils import save_json
    
    for filename, data in analytics_data.items():
        save_path = os.path.join(base_dir, filename)
        save_json(data, save_path)
        
    return True

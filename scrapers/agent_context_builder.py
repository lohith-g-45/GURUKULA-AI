import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.json_utils import save_json, load_json
from config import EXAM_CONFIG


def get_exam_dataset_path(exam_name, data_type):
    return os.path.join("datasets", exam_name, data_type)


def load_exam_metadata(exam_name):
    metadata_path = os.path.join(get_exam_dataset_path(exam_name, "exams"), f"{exam_name}_metadata.json")
    if os.path.exists(metadata_path):
        return load_json(metadata_path)
    return None


def load_syllabus(exam_name):
    syllabus_path = os.path.join(get_exam_dataset_path(exam_name, "syllabus"), f"{exam_name}_syllabus.json")
    if os.path.exists(syllabus_path):
        return load_json(syllabus_path)
    return None


def load_weightage(exam_name):
    weightage_path = os.path.join(get_exam_dataset_path(exam_name, "weightage"), f"{exam_name}_weightage.json")
    if os.path.exists(weightage_path):
        return load_json(weightage_path)
    return None


def load_pattern(exam_name):
    pattern_path = os.path.join(get_exam_dataset_path(exam_name, "patterns"), f"{exam_name}_pattern.json")
    if os.path.exists(pattern_path):
        return load_json(pattern_path)
    return None


def load_pyq_trends(exam_name):
    pyq_trends_path = os.path.join(get_exam_dataset_path(exam_name, "analytics"), "pyq_trends.json")
    if os.path.exists(pyq_trends_path):
        return load_json(pyq_trends_path)
    return None


def build_full_context(exam_name):
    return {
        "metadata": load_exam_metadata(exam_name),
        "syllabus": load_syllabus(exam_name),
        "weightage": load_weightage(exam_name),
        "pattern": load_pattern(exam_name),
        "pyq_trends": load_pyq_trends(exam_name)
    }


def build_research_agent_context(exam_name):
    full = build_full_context(exam_name)
    return {
        "agent_name": "Research Agent",
        "exam": exam_name,
        "purpose": f"Gather and synthesize {exam_name} exam intelligence",
        "focus_areas": [
            f"{exam_name} exam pattern and syllabus",
            "Subject weightage and priority",
            "PYQ trends and frequently asked topics"
        ],
        "data": {
            "metadata": full.get("metadata"),
            "syllabus": full.get("syllabus"),
            "pattern": full.get("pattern"),
            "pyq_trends": full.get("pyq_trends")
        },
        "tasks": [
            f"Summarize the complete {exam_name} exam structure",
            "Identify high-priority subjects based on weightage",
            "Analyze frequently asked topics from PYQs"
        ]
    }


def build_planning_agent_context(exam_name):
    full = build_full_context(exam_name)
    return {
        "agent_name": "Planning Agent",
        "exam": exam_name,
        "purpose": f"Create structured {exam_name} preparation roadmaps",
        "focus_areas": [
            "Time allocation",
            "Subject sequencing",
            "Weekly study targets"
        ],
        "data": {
            "subject_priority": load_json(os.path.join(get_exam_dataset_path(exam_name, "analytics"), "subject_priority.json")),
            "prep_difficulty": load_json(os.path.join(get_exam_dataset_path(exam_name, "analytics"), "preparation_difficulty.json")),
            "pattern": full.get("pattern"),
            "syllabus": full.get("syllabus")
        },
        "tasks": [
            "Create a 3-month preparation roadmap",
            "Prioritize subjects and topics",
            "Allocate study time per subject"
        ]
    }


def build_revision_agent_context(exam_name):
    full = build_full_context(exam_name)
    return {
        "agent_name": "Revision Agent",
        "exam": exam_name,
        "purpose": f"Optimize {exam_name} revision and practice",
        "focus_areas": [
            "Weak areas",
            "High-frequency topics",
            "Revision scheduling"
        ],
        "data": {
            "revision_priority": load_json(os.path.join(get_exam_dataset_path(exam_name, "analytics"), "revision_priority.json")),
            "topic_frequency": load_json(os.path.join(get_exam_dataset_path(exam_name, "analytics"), "topic_frequency.json")),
            "pyq_trends": full.get("pyq_trends"),
            "syllabus": full.get("syllabus")
        },
        "tasks": [
            "Create weekly revision plans",
            "Identify high-yield topics",
            "Recommend practice questions"
        ]
    }


def build_insight_agent_context(exam_name):
    full = build_full_context(exam_name)
    return {
        "agent_name": "Insight Agent",
        "exam": exam_name,
        "purpose": f"Extract {exam_name} trends and actionable insights",
        "focus_areas": [
            "Exam patterns",
            "Success factors",
            "Preparation strategies"
        ],
        "data": {
            "pyq_trends": full.get("pyq_trends"),
            "subject_priority": load_json(os.path.join(get_exam_dataset_path(exam_name, "analytics"), "subject_priority.json")),
            "weightage": full.get("weightage"),
            "metadata": full.get("metadata")
        },
        "tasks": [
            "Identify trends over the years",
            "Recommend preparation strategies",
            "Find patterns in PYQs"
        ]
    }


def build_agent_context(exam_name, agent_type):
    agent_builders = {
        "research": build_research_agent_context,
        "planning": build_planning_agent_context,
        "revision": build_revision_agent_context,
        "insight": build_insight_agent_context,
        "full": build_full_context
    }
    if agent_type in agent_builders:
        return agent_builders[agent_type](exam_name)
    return build_full_context(exam_name)


def build_all_agent_contexts(exam_name):
    agents = ["research", "planning", "revision", "insight", "full"]
    contexts_dir = get_exam_dataset_path(exam_name, "agent_contexts")
    os.makedirs(contexts_dir, exist_ok=True)
    
    for agent in agents:
        print(f"Building context for {agent} agent for {exam_name}...")
        context = build_agent_context(exam_name, agent)
        save_path = os.path.join(contexts_dir, f"{agent}_agent_context.json")
        save_json(context, save_path)
        print(f"Saved to {save_path}")
    
    print(f"All {exam_name} agent contexts generated successfully!")


def main():
    print("=" * 70)
    print("GURUKULA AI - AGENT CONTEXT BUILDER")
    print("=" * 70)
    
    for exam_name in EXAM_CONFIG.keys():
        print(f"\nProcessing {exam_name}...")
        try:
            build_all_agent_contexts(exam_name)
        except Exception as e:
            print(f"Error processing {exam_name}: {e}")
    
    print("\n" + "=" * 70)
    print("ALL AGENT CONTEXTS GENERATED SUCCESSFULLY!")
    print("=" * 70)


if __name__ == "__main__":
    main()

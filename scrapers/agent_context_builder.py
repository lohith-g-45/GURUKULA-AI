import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.json_utils import save_json, load_json


def load_exam_metadata():
    file_path = "datasets/exams/kas_metadata.json"
    if os.path.exists(file_path):
        return load_json(file_path)
    return None


def load_syllabus():
    file_path = "datasets/syllabus/kas_syllabus.json"
    if os.path.exists(file_path):
        return load_json(file_path)
    return None


def load_weightage():
    file_path = "datasets/weightage/kas_weightage.json"
    if os.path.exists(file_path):
        return load_json(file_path)
    return None


def load_pattern():
    file_path = "datasets/patterns/kas_pattern.json"
    if os.path.exists(file_path):
        return load_json(file_path)
    return None


def load_pyq_trends():
    file_path = "datasets/analytics/pyq_trends.json"
    if os.path.exists(file_path):
        return load_json(file_path)
    return None


def load_subject_priority():
    file_path = "datasets/analytics/subject_priority.json"
    if os.path.exists(file_path):
        return load_json(file_path)
    return None


def load_revision_priority():
    file_path = "datasets/analytics/revision_priority.json"
    if os.path.exists(file_path):
        return load_json(file_path)
    return None


def load_topic_frequency():
    file_path = "datasets/analytics/topic_frequency.json"
    if os.path.exists(file_path):
        return load_json(file_path)
    return None


def load_prep_difficulty():
    file_path = "datasets/analytics/preparation_difficulty.json"
    if os.path.exists(file_path):
        return load_json(file_path)
    return None


def build_full_context():
    return {
        "metadata": load_exam_metadata(),
        "syllabus": load_syllabus(),
        "weightage": load_weightage(),
        "pattern": load_pattern(),
        "pyq_trends": load_pyq_trends(),
        "subject_priority": load_subject_priority(),
        "revision_priority": load_revision_priority(),
        "topic_frequency": load_topic_frequency(),
        "prep_difficulty": load_prep_difficulty()
    }


def build_research_agent_context():
    full = build_full_context()
    return {
        "agent_name": "Research Agent",
        "purpose": "Gather and synthesize exam intelligence",
        "focus_areas": [
            "KAS exam pattern and syllabus",
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
            "Summarize the complete KAS exam structure",
            "Identify high-priority subjects based on weightage",
            "Analyze frequently asked topics from PYQs"
        ]
    }


def build_planning_agent_context():
    full = build_full_context()
    return {
        "agent_name": "Planning Agent",
        "purpose": "Create structured preparation roadmaps",
        "focus_areas": [
            "Time allocation",
            "Subject sequencing",
            "Weekly study targets"
        ],
        "data": {
            "subject_priority": full.get("subject_priority"),
            "prep_difficulty": full.get("prep_difficulty"),
            "pattern": full.get("pattern"),
            "syllabus": full.get("syllabus")
        },
        "tasks": [
            "Create a 3-month preparation roadmap",
            "Prioritize subjects and topics",
            "Allocate study time per subject"
        ]
    }


def build_revision_agent_context():
    full = build_full_context()
    return {
        "agent_name": "Revision Agent",
        "purpose": "Optimize revision and practice",
        "focus_areas": [
            "Weak areas",
            "High-frequency topics",
            "Revision scheduling"
        ],
        "data": {
            "revision_priority": full.get("revision_priority"),
            "topic_frequency": full.get("topic_frequency"),
            "pyq_trends": full.get("pyq_trends"),
            "syllabus": full.get("syllabus")
        },
        "tasks": [
            "Create weekly revision plans",
            "Identify high-yield topics",
            "Recommend practice questions"
        ]
    }


def build_insight_agent_context():
    full = build_full_context()
    return {
        "agent_name": "Insight Agent",
        "purpose": "Extract trends and actionable insights",
        "focus_areas": [
            "Exam patterns",
            "Success factors",
            "Preparation strategies"
        ],
        "data": {
            "pyq_trends": full.get("pyq_trends"),
            "subject_priority": full.get("subject_priority"),
            "weightage": full.get("weightage"),
            "metadata": full.get("metadata")
        },
        "tasks": [
            "Identify trends over the years",
            "Recommend preparation strategies",
            "Find patterns in PYQs"
        ]
    }


def build_agent_context(agent_type):
    agent_builders = {
        "research": build_research_agent_context,
        "planning": build_planning_agent_context,
        "revision": build_revision_agent_context,
        "insight": build_insight_agent_context,
        "full": build_full_context
    }
    if agent_type in agent_builders:
        return agent_builders[agent_type]()
    return build_full_context()


def main():
    print("=" * 70)
    print("GURUKULA AI - AGENT CONTEXT BUILDER")
    print("=" * 70)
    
    os.makedirs("datasets/agent_contexts", exist_ok=True)
    
    agents = ["research", "planning", "revision", "insight", "full"]
    for agent in agents:
        print(f"\nBuilding context for {agent} agent...")
        context = build_agent_context(agent)
        save_path = f"datasets/agent_contexts/{agent}_agent_context.json"
        save_json(context, save_path)
        print(f"OK: Saved to {save_path}")
    
    print("\n" + "=" * 70)
    print("ALL AGENT CONTEXTS GENERATED SUCCESSFULLY!")
    print("These contexts are ready for AI APIs (Gemini/OpenAI).")
    print("=" * 70)


if __name__ == "__main__":
    main()

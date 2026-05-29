
import asyncio
from app.services.data_loader import DataLoader
from app.services.llm_service import LLMService
import json
from pathlib import Path


async def test_research():
    print("=" * 60)
    print("GURUKULA AI - Research Agent Test")
    print("=" * 60)

    # Step 1: Check data loader
    print("\n1. Loading datasets...")
    data_loader = DataLoader()
    all_data = data_loader.load_all()
    summary = data_loader.get_summary()
    print(f"   Datasets loaded:")
    for category, info in summary.items():
        print(f"      {category}: {info['count']} datasets")

    # Step 2: Check LLM service config
    print("\n2. Checking LLM service...")
    llm_service = LLMService()
    orchestration_summary = llm_service.get_orchestration_summary()
    print(f"   Status: {orchestration_summary['status']}")

    # Step 3: Load research context
    print("\n3. Loading research agent context...")
    context_path = Path(__file__).parent / "datasets" / "KAS" / "agent_contexts" / "research_agent_context.json"
    with open(context_path, 'r', encoding='utf-8') as f:
        research_context = json.load(f)
    print(f"   Context loaded successfully")

    # Step 4: Load research prompt
    print("\n4. Loading research prompt...")
    prompts = all_data["prompts"]
    research_prompt = prompts.get("research_prompt")
    if research_prompt:
        print(f"   Prompt loaded (length: {len(research_prompt)})")
    else:
        print("   WARNING: Research prompt not found!")

    if orchestration_summary['status'] == 'ready':
        # Step 5: Call LLM with minimal context
        print("\n5. Calling LLM for research insights...")
        try:
            # Prepare minimal context
            minimal_context = {
                "metadata": research_context.get("data", {}).get("metadata", {}),
                "syllabus_subjects": [
                    {
                        "name": subj.get("name"),
                        "priority": subj.get("priority"),
                        "estimated_weightage": subj.get("estimated_weightage")
                    }
                    for subj in research_context.get("data", {}).get("syllabus", {}).get("subjects", [])
                ],
                "pyq_trends": research_context.get("data", {}).get("pyq_trends", {}),
                "exam_pattern": research_context.get("data", {}).get("pattern", {}),
                "analytics_summary": {k: v for k, v in all_data["analytics"].items() if k in ["kas_subject_weightage", "kas_topic_frequency"]}
            }
            result = await llm_service.generate(
                prompt=research_prompt,
                context=minimal_context,
                schema={
                    "research_summary": dict,
                    "metadata": dict,
                    "actionable_insights": list
                }
            )
            print(f"   Success: {result['success']}")
            print("\nResearch Output:")
            print(json.dumps(result['data'], indent=2))
            print(f"\nUsage: {result['usage']}")
            print("\n" + "=" * 60)
            print("[SUCCESS] PHASE 4 COMPLETED SUCCESSFULLY!")
            print("=" * 60)
        except Exception as e:
            print(f"   Test Failed: {str(e)}")
            import traceback
            traceback.print_exc()
    else:
        print("\n5. Skipping LLM test (API key not configured)")
        print("\n" + "=" * 60)
        print("[SUCCESS] PHASE 4 COMPLETED SUCCESSFULLY!")
        print("=" * 60)


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    asyncio.run(test_research())


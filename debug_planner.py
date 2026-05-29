
import asyncio
import json
from pathlib import Path
from groq import AsyncGroq
from app.config.settings import settings
from app.services.data_loader import DataLoader


async def debug_planner_call():
    print("=" * 100)
    print("DEBUG: PLANNER API GROQ CALL")
    print("=" * 100)

    # Step 1: Load all data
    data_loader = DataLoader()
    all_data = data_loader.load_all()
    prompts = all_data["prompts"]
    planning_data = all_data["planning"]

    # Load planning agent context using DataLoader's base path
    context_path = data_loader.base_path / "agent_contexts" / "planning_agent_context.json"
    print(f"[DEBUG] Loading context from: {context_path}")
    with open(context_path, 'r', encoding='utf-8') as f:
        planning_context = json.load(f)

    # Step 2: Build minimal context (EXACTLY as in planning route)
    minimal_context = {
        "readiness_score": 70.0,
        "available_hours_per_day": 6.0,
        "exam_date_distance_days": 180,
        "weak_subjects": ["History", "Geography"],
        "metadata": planning_context.get("data", {}).get("metadata", {}),
        "syllabus_subjects": [
            {
                "name": subj.get("name"),
                "priority": subj.get("priority"),
                "estimated_weightage": subj.get("estimated_weightage")
            }
            for subj in planning_context.get("data", {}).get("syllabus", {}).get("subjects", [])
        ],
        "exam_pattern": planning_context.get("data", {}).get("pattern", {}),
        "roadmap_rules": planning_data.get("roadmap_rules", {}),
        "adaptive_planning_rules": planning_data.get("adaptive_planning_rules", {}),
        "revision_cycles": planning_data.get("revision_cycles", {}),
        "mock_planning_rules": planning_data.get("mock_planning_rules", {})
    }

    # Step 3: Build full prompt (EXACTLY as in LLMService)
    base_prompt = prompts.get("planning_prompt", "")
    full_prompt = base_prompt
    # Inject context (same as PromptInjector.inject_context)
    context_str = "\n\n=== CONTEXT ===\n"
    for key, value in minimal_context.items():
        context_str += f"{key}:\n{json.dumps(value, indent=2)}\n\n"
    full_prompt += context_str
    full_prompt += "\n\nPlease respond only in valid JSON format only, no additional text."

    # Step 4: Print prompt info
    print(f"\n[DEBUG] PROMPT INFO:")
    print(f"  Character Count: {len(full_prompt)}")
    approx_tokens = len(full_prompt) // 4
    print(f"  Approx Token Count (1 char ~ 0.25 tokens): {approx_tokens}")
    print(f"  Model: {settings.GROQ_MODEL}")

    # Step 5: Call Groq DIRECTLY - NO RETRIES!
    try:
        print(f"\n[DEBUG] CALLING GROQ...")
        client = AsyncGroq(api_key=settings.GROQ_API_KEY)
        chat_completion = await client.chat.completions.create(
            messages=[{"role": "user", "content": full_prompt}],
            model=settings.GROQ_MODEL,
            temperature=settings.GROQ_TEMPERATURE,
            max_tokens=settings.GROQ_MAX_TOKENS,
            response_format={"type": "json_object"}
        )
        print(f"\n[DEBUG] GROQ SUCCESS!")
        print(f"  Usage: {chat_completion.usage}")
    except Exception as e:
        print(f"\n[DEBUG] GROQ FAILED!")
        print(f"  Exception Type: {type(e).__name__}")
        print(f"  Exception Message: {str(e)}")
        print(f"\n  FULL TRACEBACK:")
        import traceback
        traceback.print_exc()
        if hasattr(e, 'status_code'):
            print(f"\n  Status Code: {e.status_code}")
        if hasattr(e, 'response'):
            print(f"\n  Response: {e.response}")
    finally:
        if 'client' in locals():
            await client.close()


if __name__ == "__main__":
    asyncio.run(debug_planner_call())

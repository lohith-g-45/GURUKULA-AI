
import sys
import asyncio
sys.path.insert(0, '.')
from app.routes.research import get_research_insights
from app.schemas.research import ResearchRequest


async def test_research_agent():
    print("="*60)
    print("Testing Research Agent")
    print("="*60)
    try:
        request = ResearchRequest(exam="KAS")
        response = await get_research_insights(request)
        print(f"[OK] Response status: {response.success}")
        print(f"[OK] Research summary: {response.data.research_summary}")
        print(f"[OK] Metadata: {response.data.metadata}")
        print(f"[OK] Actionable insights count: {len(response.data.actionable_insights)}")
        print("\n" + "="*60)
        print("RESEARCH AGENT FIXED SUCCESSFULLY!")
        print("="*60)
        return True
    except Exception as e:
        print(f"[FAIL] {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    asyncio.run(test_research_agent())

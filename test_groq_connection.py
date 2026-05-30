
import asyncio
import json
from app.services.llm_service import LLMService
from app.config.settings import settings

async def main():
    print("=== Checking Configuration ===")
    print(f"API Key Loaded: {bool(settings.GROQ_API_KEY)}")
    print(f"Model Name: {settings.GROQ_MODEL}")

    llm_service = LLMService()
    config_status = llm_service.config.get_status()
    print(f"Config Status: {config_status}")

    if not config_status['api_key_configured']:
        print("\nERROR: API key not configured!")
        return

    print("\n=== Running Hello World Test ===")
    try:
        test_result = await llm_service.generate(
            prompt="Generate a JSON with a 'message' field saying 'Hello GURUKULA AI!'",
            schema={"message": str}
        )
        print(f"Test Success: {test_result['success']}")
        if test_result['success']:
            print(f"Response: {json.dumps(test_result['data'], indent=2)}")
            print(f"Usage: {test_result['usage']}")
        else:
            print(f"Error: {test_result['error']}")
    except Exception as e:
        print(f"\nTest Failed: {type(e).__name__} - {str(e)}")
        import traceback
        traceback.print_exc()
        if hasattr(e, 'response'):
            print(f"Response Status: {e.response.status_code}")
            print(f"Response Body: {e.response.text}")

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())

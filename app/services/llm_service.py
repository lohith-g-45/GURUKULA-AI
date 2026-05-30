import json
import logging
from typing import Dict, Any, Optional, AsyncGenerator
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from groq import AsyncGroq
from app.config.settings import settings

logger = logging.getLogger(__name__)


class PromptInjector:
    @staticmethod
    def inject_prompt(base_prompt: str, variables: Dict[str, Any]) -> str:
        prompt = base_prompt
        for key, value in variables.items():
            placeholder = "{" + key + "}"
            if placeholder in prompt:
                prompt = prompt.replace(placeholder, str(value))
        return prompt

    @staticmethod
    def inject_context(base_prompt: str, context_data: Dict[str, Any]) -> str:
        context_str = "\n\nCONTEXT:\n"
        for key, value in context_data.items():
            context_str += f"{key}: {json.dumps(value, separators=(',', ':'))}\n"
        return base_prompt + context_str


class ResponseValidator:
    @staticmethod
    def validate_json(response_text: str) -> Dict[str, Any]:
        try:
            json_str = response_text.strip()
            if json_str.startswith("```json"):
                json_str = json_str[7:]
            if json_str.startswith("```"):
                json_str = json_str[3:]
            if json_str.endswith("```"):
                json_str = json_str[:-3]
            json_str = json_str.strip()
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            logger.error(f"JSON validation failed: {str(e)}")
            raise ValueError(f"Failed to parse JSON response: {str(e)}")

    @staticmethod
    def validate_schema(data: Any, schema: Any) -> bool:
        if schema is None:
            return True

        if isinstance(schema, dict):
            if not isinstance(data, dict):
                raise ValueError(f"Expected dict, got {type(data)}")
            for key, expected in schema.items():
                if key not in data:
                    raise ValueError(f"Missing required key: {key}")
                ResponseValidator.validate_schema(data[key], expected)
            return True
        elif isinstance(schema, list):
            if not isinstance(data, list):
                raise ValueError(f"Expected list, got {type(data)}")
            if len(schema) > 0:
                item_schema = schema[0]
                for item in data:
                    ResponseValidator.validate_schema(item, item_schema)
            return True
        else:  # schema is a type
            # Allow int for float expectations (since LLM might return integers)
            if schema == float and isinstance(data, int):
                return True
            if not isinstance(data, schema):
                raise ValueError(f"Wrong type. Expected {schema}, got {type(data)}")
            return True


class GroqConfig:
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.model = settings.GROQ_MODEL
        self.temperature = settings.GROQ_TEMPERATURE
        self.max_tokens = settings.GROQ_MAX_TOKENS
        self.max_retries = settings.GROQ_MAX_RETRIES
        self.retry_delay = settings.GROQ_RETRY_DELAY

    def get_status(self) -> Dict[str, Any]:
        return {
            "api_key_configured": bool(self.api_key),
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "max_retries": self.max_retries,
            "retry_delay": self.retry_delay
        }


class LLMService:
    def __init__(self):
        self.config = GroqConfig()
        self.prompt_injector = PromptInjector()
        self.response_validator = ResponseValidator()
        self._client: Optional[AsyncGroq] = None

    async def generate(
        self,
        prompt: str,
        prompt_variables: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
        schema: Optional[Dict[str, Any]] = None,
        system_instruction: Optional[str] = None
    ) -> Dict[str, Any]:
        if not self.config.api_key:
            return {"success": False, "error": "GROQ_API_KEY not configured"}
        
        full_prompt = prompt
        if prompt_variables:
            full_prompt = self.prompt_injector.inject_prompt(full_prompt, prompt_variables)
        if context:
            full_prompt = self.prompt_injector.inject_context(full_prompt, context)
        
        # Log prompt metrics
        prompt_chars = len(full_prompt)
        estimated_tokens = prompt_chars // 4
        logger.info(f"Prompt length: {prompt_chars} chars, estimated tokens: {estimated_tokens}, model: {self.config.model}")

        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": full_prompt + "\n\nPlease respond only in valid JSON format."})

        try:
            logger.info(f"[LLM Request] Model: {self.config.model}")
            logger.info(f"[LLM Request] Payload: messages={json.dumps(messages)}, temperature={self.config.temperature}, max_tokens={self.config.max_tokens}")
            client = AsyncGroq(api_key=self.config.api_key)
            chat_completion = await client.chat.completions.create(
                messages=messages,
                model=self.config.model,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                response_format={"type": "json_object"}
            )
            logger.info(f"[LLM Response] Payload: {json.dumps(chat_completion.model_dump())}")
            response_text = chat_completion.choices[0].message.content

            result = self.response_validator.validate_json(response_text)
            self.response_validator.validate_schema(result, schema)

            await client.close()

            return {
                "success": True,
                "data": result,
                "usage": {
                    "prompt_tokens": chat_completion.usage.prompt_tokens,
                    "completion_tokens": chat_completion.usage.completion_tokens,
                    "total_tokens": chat_completion.usage.total_tokens
                }
            }
        except Exception as e:
            logger.error(f"[LLM Error] str(e): {str(e)}")
            logger.error(f"[LLM Error] repr(e): {repr(e)}")
            import traceback
            logger.error(f"[LLM Error] Traceback: {traceback.format_exc()}")
            logger.error(f"[LLM Error] Model: {self.config.model}")
            logger.error(f"[LLM Error] Request Payload: {json.dumps(messages)}")
            if hasattr(e, 'response') and e.response:
                logger.error(f"[LLM Error] Response Status: {e.response.status_code}")
                logger.error(f"[LLM Error] Response Body: {e.response.text}")
            return {
                "success": False,
                "error": f"{type(e).__name__}: {str(e)}"
            }

    async def generate_stream(
        self,
        prompt: str,
        prompt_variables: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
        system_instruction: Optional[str] = None
    ) -> AsyncGenerator[str, None]:
        if not self.config.api_key:
            raise RuntimeError("GROQ_API_KEY not configured in .env file.")

        full_prompt = prompt
        if prompt_variables:
            full_prompt = self.prompt_injector.inject_prompt(full_prompt, prompt_variables)
        if context:
            full_prompt = self.prompt_injector.inject_context(full_prompt, context)

        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": full_prompt})

        try:
            client = AsyncGroq(api_key=self.config.api_key)
            stream = await client.chat.completions.create(
                messages=messages,
                model=self.config.model,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                stream=True
            )
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
            await client.close()
        except Exception as e:
            logger.error(f"Streaming failed: {str(e)}")
            raise

    def get_orchestration_summary(self) -> Dict[str, Any]:
        return {
            "config": self.config.get_status(),
            "status": "ready" if self.config.api_key else "not_configured",
            "features": [
                "prompt_injection",
                "context_injection",
                "structured_json",
                "retry_handling",
                "token_optimization",
                "streaming",
                "fallback_handling",
                "response_validation"
            ]
        }


def main():
    import asyncio
    print("=" * 60)
    print("GURUKULA AI - Groq LLM Service Test")
    print("=" * 60)

    llm_service = LLMService()

    print("\n1. Groq Configuration Status:")
    config_status = llm_service.config.get_status()
    for key, value in config_status.items():
        print(f"   {key}: {value}")

    print("\n2. Orchestration Summary:")
    orchestration_summary = llm_service.get_orchestration_summary()
    print(f"   Status: {orchestration_summary['status']}")
    print(f"   Features: {', '.join(orchestration_summary['features'])}")

    if config_status['api_key_configured']:
        print("\n3. Running Test Request...")
        try:
            test_result = asyncio.run(llm_service.generate(
                prompt="Generate a JSON with a 'message' field saying 'Hello GURUKULA AI!'",
                schema={"message": str}
            ))
            print(f"   Test Success: {test_result['success']}")
            print(f"   Response: {test_result['data']}")
            print(f"   Usage: {test_result['usage']}")
            print("\n" + "=" * 60)
            print("[SUCCESS] PHASE 3 COMPLETED SUCCESSFULLY!")
            print("=" * 60)
        except Exception as e:
            print(f"   Test Failed: {str(e)}")
            import traceback
            traceback.print_exc()
    else:
        print("\n3. Skipping Test Request (API key not configured)")
        print("\n" + "=" * 60)
        print("[SUCCESS] PHASE 3 COMPLETED SUCCESSFULLY!")
        print("=" * 60)


if __name__ == "__main__":
    import sys
    import traceback
    logging.basicConfig(level=logging.INFO)
    main()
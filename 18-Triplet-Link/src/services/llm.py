from openai import OpenAI
import os
from src.config import config
from tenacity import retry, stop_after_attempt, wait_exponential

class LLMService:
    def __init__(self):
        self._client = None

    @property
    def client(self):
        if self._client is None:
            api_key = config.OPENAI_API_KEY
            if not api_key:
                # Fallback for testing or if env not loaded yet
                api_key = os.getenv("OPENAI_API_KEY")
            
            if not api_key:
                # For testing purposes, we might want to allow instantiation but fail on call
                # Or just print warning
                print("Warning: OPENAI_API_KEY not found.")
                api_key = "dummy_key_for_testing"
                
            self._client = OpenAI(
                api_key=api_key, 
                base_url=config.OPENAI_BASE_URL if config.OPENAI_BASE_URL else "https://api.openai.com/v1"
            )
        return self._client

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def chat_completion(self, messages, model=None, temperature=0.0, response_format=None):
        if model is None:
            model = config.OPENAI_MODEL_NAME
            
        try:
            kwargs = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
            }
            if response_format:
                kwargs["response_format"] = response_format
                
            response = self.client.chat.completions.create(**kwargs)
            return response.choices[0].message.content
        except Exception as e:
            print(f"LLM Error: {e}")
            raise

llm_service = LLMService()

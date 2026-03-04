import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    MODEL_NAME = os.getenv("MODEL_NAME")
    REST_COUNTRIES_BASE_URL = "https://restcountries.com/v3.1/name"

    @classmethod
    def validate(cls):
        if cls.LLM_PROVIDER == "openai" and not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is missing for OpenAI provider.")
        elif cls.LLM_PROVIDER == "gemini" and not cls.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY environment variable is missing for Gemini provider.")
        elif cls.LLM_PROVIDER not in ["openai", "gemini"]:
            raise ValueError(f"Unsupported LLM_PROVIDER: {cls.LLM_PROVIDER}. Choose 'openai' or 'gemini'.")
"""
AI abstraction layer. All AI features (roadmap generation, tutor Q&A, quiz
generation, notes generation, skill-gap analysis) call through this module,
so swapping Gemini for OpenAI later only means editing this one file.
"""
import json

from app.core.config import settings


class AIProvider:
    async def generate(self, prompt: str, *, json_mode: bool = False) -> str:
        raise NotImplementedError


class GeminiProvider(AIProvider):
    def __init__(self) -> None:
        import google.generativeai as genai
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self._genai = genai
        self._model = genai.GenerativeModel("gemini-1.5-flash")

    async def generate(self, prompt: str, *, json_mode: bool = False) -> str:
        generation_config = {"response_mime_type": "application/json"} if json_mode else {}
        response = self._model.generate_content(prompt, generation_config=generation_config)
        return response.text


class MockProvider(AIProvider):
    """Used automatically when no GEMINI_API_KEY is configured, so the rest of the
    app (and the frontend) remains fully functional in a fresh dev environment."""

    async def generate(self, prompt: str, *, json_mode: bool = False) -> str:
        if json_mode:
            return json.dumps({
                "note": "Mock AI response — set GEMINI_API_KEY in backend/.env for real output.",
                "prompt_received": prompt[:200],
            })
        return (
            "This is a placeholder AI response. Configure GEMINI_API_KEY in backend/.env "
            "to get real answers from Gemini."
        )


def get_ai_provider() -> AIProvider:
    if settings.AI_PROVIDER == "gemini" and settings.GEMINI_API_KEY:
        return GeminiProvider()
    return MockProvider()

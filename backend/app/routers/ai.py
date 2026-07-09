"""
AI-powered features: learning-path generator, tutor chatbot, quiz generator,
notes generator, and skill-gap analysis. All routed through AIProvider so the
underlying model (Gemini today, optionally OpenAI later) is a one-line swap.
"""
from fastapi import APIRouter, Depends

from app.core.deps import get_current_user
from app.models.user import UserInDB
from app.services.ai_provider import get_ai_provider

router = APIRouter(prefix="/ai", tags=["AI Features"])


@router.post("/roadmap")
async def generate_roadmap(
    goal: str, current_skill_level: str, available_hours_per_week: float,
    current_user: UserInDB = Depends(get_current_user),
):
    provider = get_ai_provider()
    prompt = (
        f"Create a personalized learning roadmap as JSON with this shape: "
        f'{{"weeks": [{{"week": 1, "focus": "...", "topics": ["..."], "estimated_hours": 0}}]}}. '
        f"Goal: {goal}. Current skill level: {current_skill_level}. "
        f"Available time: {available_hours_per_week} hours/week. Keep it realistic and specific."
    )
    result = await provider.generate(prompt, json_mode=True)
    return {"roadmap": result}


@router.post("/tutor")
async def ask_tutor(question: str, context_material: str, current_user: UserInDB = Depends(get_current_user)):
    provider = get_ai_provider()
    prompt = (
        f"You are a helpful tutor. Answer the student's question using ONLY the material below. "
        f"If the answer isn't in the material, say so.\n\nMaterial:\n{context_material}\n\nQuestion: {question}"
    )
    answer = await provider.generate(prompt)
    return {"answer": answer}


@router.post("/generate-quiz")
async def generate_quiz(source_text: str, num_questions: int = 5, current_user: UserInDB = Depends(get_current_user)):
    provider = get_ai_provider()
    prompt = (
        f"Generate {num_questions} quiz questions (mix of mcq/true_false/short_answer) from this material, "
        f'as JSON: {{"questions": [{{"question": "...", "type": "mcq", "options": ["..."], '
        f'"correct_answer": "...", "points": 1}}]}}.\n\nMaterial:\n{source_text}'
    )
    result = await provider.generate(prompt, json_mode=True)
    return {"quiz": result}


@router.post("/generate-notes")
async def generate_notes(source_text: str, current_user: UserInDB = Depends(get_current_user)):
    provider = get_ai_provider()
    prompt = f"Summarize this material into concise, well-structured study notes with headings and bullet points:\n\n{source_text}"
    notes = await provider.generate(prompt)
    return {"notes": notes}


@router.post("/skill-gap-analysis")
async def skill_gap_analysis(
    current_skills: list[str], target_role: str, current_user: UserInDB = Depends(get_current_user),
):
    provider = get_ai_provider()
    prompt = (
        f"Compare these current skills: {current_skills} against requirements for the role '{target_role}'. "
        f'Return JSON: {{"gaps": ["..."], "matching_skills": ["..."], "recommended_courses": ["..."]}}.'
    )
    result = await provider.generate(prompt, json_mode=True)
    return {"analysis": result}

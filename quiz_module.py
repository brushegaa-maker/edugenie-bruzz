import json
import re

from pydantic import ValidationError

from gemini_client import generate_text
from schemas import QuizQuestion, QuizResponse


def clean_json_block(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def generate_quiz(text: str) -> QuizResponse:
    prompt = f"""
Generate exactly 3 multiple-choice questions from the educational content below.

Content:
{text}

Return ONLY valid JSON in this exact shape:
{{
  "questions": [
    {{
      "question": "string",
      "options": ["option A", "option B", "option C", "option D"],
      "answer": "the exact correct option text",
      "explanation": "one short explanation"
    }}
  ]
}}

Rules:
- Exactly 3 questions.
- Exactly 4 options per question.
- One correct answer.
- Questions must be answerable from the supplied content.
- Make distractors plausible but clearly incorrect.
"""
    raw = generate_text(
        prompt,
        system_instruction="You generate strict JSON for an educational quiz.",
        temperature=0.3,
        response_mime_type="application/json",
    )
    cleaned = clean_json_block(raw)

    try:
        data = json.loads(cleaned)
        result = QuizResponse.model_validate(data)
    except (json.JSONDecodeError, ValidationError) as exc:
        raise RuntimeError(f"Quiz response could not be parsed as valid JSON: {exc}") from exc

    if len(result.questions) != 3:
        raise RuntimeError("Gemini returned a quiz with an incorrect number of questions.")

    for q in result.questions:
        if q.answer not in q.options:
            raise RuntimeError("Quiz answer must exactly match one of the four options.")

    return result

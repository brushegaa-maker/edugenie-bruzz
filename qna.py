from gemini_client import generate_text


def answer_question(question: str) -> str:
    prompt = f"""
Answer the student's question below.

Student question:
{question}

Requirements:
- Give a correct, concise educational answer.
- Explain unfamiliar terms briefly.
- Use simple language suitable for a student.
- If the question is ambiguous, state the assumption you made.
"""
    return generate_text(
        prompt,
        system_instruction="You are EduGenie, a patient educational assistant.",
        temperature=0.2,
    )

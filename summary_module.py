from gemini_client import generate_text


def summarize_text(text: str) -> str:
    prompt = f"""
Summarize the following educational passage for a student.

Passage:
{text}

Requirements:
- Keep the important facts and relationships.
- Remove repetition and unnecessary detail.
- Use short paragraphs or bullet points when helpful.
- Do not introduce facts that are not supported by the passage.
"""
    return generate_text(
        prompt,
        system_instruction="You are an educational summarization assistant.",
        temperature=0.2,
    )

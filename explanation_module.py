from functools import lru_cache

from config import settings
from gemini_client import generate_text


@lru_cache(maxsize=1)
def _local_pipeline():
    from transformers import pipeline

    return pipeline(
        "text2text-generation",
        model=settings.local_explainer_model,
        device=-1,
    )


def _local_explain(topic: str) -> str:
    generator = _local_pipeline()
    prompt = (
        "Explain this topic to a beginner in simple language. "
        "Use a short definition, a simple example, and 3 key points. "
        f"Topic: {topic}"
    )
    output = generator(prompt, max_new_tokens=220, do_sample=False)
    return output[0]["generated_text"].strip()


def _gemini_explain(topic: str) -> str:
    prompt = f"""
Explain the following topic to a beginner:

{topic}

Use this structure:
- Simple definition
- How it works
- Easy real-world/example analogy
- 3 key points
- One common mistake or misconception

Keep the explanation clear and concise.
"""
    return generate_text(
        prompt,
        system_instruction="You are EduGenie explaining difficult concepts to beginners.",
        temperature=0.3,
    )


def explain_concept(topic: str) -> str:
    if settings.use_local_explainer:
        try:
            return _local_explain(topic)
        except Exception:
            # The local model is optional; fall back to Gemini so the endpoint
            # remains useful if the model is unavailable on the machine.
            return _gemini_explain(topic)
    return _gemini_explain(topic)

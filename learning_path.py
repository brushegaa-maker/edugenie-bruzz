from gemini_client import generate_text


def get_learning_recommendations(topic: str) -> str:
    prompt = f"""
Create a personalized learning path for this topic:

{topic}

Structure the answer as:
1. Goal
2. Beginner foundations
3. Intermediate topics
4. Advanced topics
5. Suggested timeline
6. Practice activities
7. Useful resource types (books, articles, videos, documentation)
8. How to check progress

Keep it practical for a student. If the learner's level is not provided,
state that the plan assumes a beginner and can be adjusted.
"""
    return generate_text(
        prompt,
        system_instruction="You are a curriculum designer who creates clear learning paths.",
        temperature=0.4,
    )

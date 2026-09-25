import time
from qna import client, MODEL_NAME

FALLBACK_MODELS = [
    "gemini-3.6-flash",
    "gemini-3.7-flash"
]


def recommend_learning_path(topic):

    prompt = f"""
Create a personalized learning path for a student who wants to learn:

Topic: {topic}

Organize the learning path from beginner to advanced.

Include:
1. Beginner level
2. Intermediate level
3. Advanced level
4. Useful resources

Keep the explanation simple and student-friendly.
"""

    models_to_try = [MODEL_NAME] + FALLBACK_MODELS

    for model in models_to_try:

        try:
            print(f"Trying Gemini model: {model}")

            response = client.models.generate_content(
                model=model,
                contents=prompt
            )

            return response.text.strip()

        except Exception as error:

            error_text = str(error)

            if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
                print(f"{model} quota exceeded.")
                continue

            if "503" in error_text or "UNAVAILABLE" in error_text:
                print(f"{model} is temporarily unavailable.")
                continue

            raise error

    return """
Learning Path temporarily unavailable because the Gemini API
free-tier quota has been reached.

Please try again after the quota resets.
"""

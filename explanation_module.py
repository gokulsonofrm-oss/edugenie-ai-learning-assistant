from qna import client, MODEL_NAME

FALLBACK_MODEL = "gemini-3.6-flash"


def explain_topic(topic):

    prompt = f"""
Explain the following topic in simple language for a student.

Topic: {topic}

Requirements:
- Start from the basics
- Use simple English
- Give a clear explanation
- Include a small example if useful
- Keep it student-friendly
"""

    models_to_try = [
        MODEL_NAME,
        FALLBACK_MODEL
    ]

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
                print(f"{model} temporarily unavailable.")
                continue

            print(f"Explanation error: {error}")
            break

    return (
        "Explanation is temporarily unavailable. "
        "Please try again after the Gemini API quota resets."
    )

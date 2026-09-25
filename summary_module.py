from qna import client, MODEL_NAME

FALLBACK_MODEL = "gemini-3.6-flash"


def summarize_text(text):

    prompt = f"""
Summarize the following text clearly and briefly for a student.

Text:
{text}

Provide the main points in simple language.
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

                print(f"{model} is temporarily unavailable.")
                continue

            print(f"Summary error: {error}")

            break

    return (
        "Summary generation is temporarily unavailable "
        "because the Gemini API quota has been reached. "
        "Please try again after the quota resets."
    )

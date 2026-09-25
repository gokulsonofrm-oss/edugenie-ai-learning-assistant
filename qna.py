import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = __import__("os").getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from .env")

client = genai.Client(api_key=api_key)

MODEL_NAME = "gemini-3.8-flash"
FALLBACK_MODEL = "gemini-3.6-flash"


def ask_gemini(question):

    models_to_try = [
        MODEL_NAME,
        FALLBACK_MODEL
    ]

    for model in models_to_try:

        try:

            print(f"Trying Gemini model: {model}")

            response = client.models.generate_content(
                model=model,
                contents=question
            )

            return response.text

        except Exception as error:

            error_text = str(error)

            if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:

                print(f"{model} quota exceeded.")
                continue

            if "503" in error_text or "UNAVAILABLE" in error_text:

                print(f"{model} is temporarily unavailable.")
                continue

            print(f"Gemini error: {error}")

            return "Sorry, an error occurred while contacting Gemini."

    return (
        "Gemini is temporarily unavailable because the API quota "
        "has been reached. Please try again after the quota resets."
    )

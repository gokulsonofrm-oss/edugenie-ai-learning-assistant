import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY) if API_KEY else None


def fallback_quiz(topic):
    return {
        "quiz": [
            {
                "question": f"What is {topic}?",
                "options": [
                    f"A concept related to {topic}",
                    "A type of hardware",
                    "A programming error",
                    "None of the above"
                ],
                "answer": f"A concept related to {topic}"
            },
            {
                "question": f"Which statement is related to {topic}?",
                "options": [
                    f"It is related to {topic}",
                    "It is only a computer game",
                    "It is a type of keyboard",
                    "It has no practical use"
                ],
                "answer": f"It is related to {topic}"
            },
            {
                "question": f"Why is {topic} useful?",
                "options": [
                    "It can help solve problems and perform useful tasks",
                    "It only changes screen brightness",
                    "It is used only for printing",
                    "It has no applications"
                ],
                "answer": "It can help solve problems and perform useful tasks"
            }
        ]
    }


def generate_quiz(topic):

    if not topic.strip():
        return {
            "quiz": []
        }

    if client is None:
        return fallback_quiz(topic)

    prompt = f"""
Create a simple educational quiz about: {topic}

Generate exactly 3 multiple-choice questions.

Return ONLY valid JSON in this format:

{{
  "quiz": [
    {{
      "question": "Question",
      "options": [
        "Option 1",
        "Option 2",
        "Option 3",
        "Option 4"
      ],
      "answer": "Correct option"
    }}
  ]
}}
"""

    models = [
        "gemini-3.8-flash",
        "gemini-3.6-flash",
        "gemini-3.7-flash"
    ]

    for model in models:

        try:

            print(f"Trying Gemini model: {model}")

            response = client.models.generate_content(
                model=model,
                contents=prompt
            )

            text = response.text.strip()

            # Remove markdown code fences if Gemini returns them
            if text.startswith("```"):
                text = text.replace("```json", "")
                text = text.replace("```", "")
                text = text.strip()

            return json.loads(text)

        except Exception as error:

            print(f"{model} failed: {error}")

            error_text = str(error).lower()

            if "quota" in error_text or "429" in error_text:
                print("Gemini quota reached. Using local fallback quiz.")
                return fallback_quiz(topic)

            continue

    print("All Gemini models failed. Using local fallback quiz.")

    return fallback_quiz(topic)
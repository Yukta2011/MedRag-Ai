import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


MODELS = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
]


def ask_cloud_model(prompt: str):
    """
    Sends a complete prompt to Gemini.
    """

    last_error = None

    for model in MODELS:

        try:

            response = client.models.generate_content(
                model=model,
                contents=prompt,
            )

            if response.text:
                return response.text.strip()

        except Exception as e:
            last_error = e

    return f"Gemini Error: {last_error}"


if __name__ == "__main__":

    prompt = "What is diabetes?"

    print(ask_cloud_model(prompt))
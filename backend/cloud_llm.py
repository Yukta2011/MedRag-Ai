import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def ask_cloud_model(prompt):
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)

        # Try current models in order (as of June 2026)
        model_names = [
            "gemini-3.5-flash",
            "gemini-3.1-pro",
            "gemini-3.1-flash",
            "gemini-3.1-flash-lite",
            "gemini-2.5-pro",
            "gemini-2.5-flash",
            "gemini-2.0-flash",
        ]

        for model_name in model_names:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                return response.text
            except Exception:
                continue

        return "Gemini Error: All model names failed. Check your API key and model access."

    except ImportError:
        return "Gemini Error: google-generativeai not installed. Run: pip install google-generativeai"
    except Exception as e:
        return f"Gemini Error: {e}"


if __name__ == "__main__":
    answer = ask_cloud_model("What is diabetes?")
    print(answer)
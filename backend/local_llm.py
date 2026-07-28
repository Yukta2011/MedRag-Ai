import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral"


def ask_local_model(prompt: str):
    """
    Sends an already-built prompt directly to Ollama.
    """

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.2,
                    "top_p": 0.9,
                    "num_predict": 700
                }
            },
            timeout=120
        )

        response.raise_for_status()

        data = response.json()

        return data.get("response", "No response from Ollama.")

    except requests.exceptions.Timeout:
        return "Error: Ollama timed out."

    except requests.exceptions.ConnectionError:
        return "Error: Could not connect to Ollama."

    except Exception as e:
        return f"Ollama Error: {e}"


if __name__ == "__main__":

    prompt = """
Explain what diabetes is.

"""

    print(ask_local_model(prompt))
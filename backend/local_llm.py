import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral"


def ask_local_model(prompt, model=None):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": model or MODEL, "prompt": prompt, "stream": False},
            timeout=300
        )
        result = response.json()
        return result["response"]
    except requests.exceptions.Timeout:
        return "Error: Ollama is taking too long. The model may be too slow for your hardware. Try a smaller model like 'phi3' or 'tinyllama'."
    except requests.exceptions.ConnectionError:
        return "Error: Ollama is not running. Start it with 'ollama serve'"
    except Exception as e:
        return f"Ollama Error: {e}"


if __name__ == "__main__":
    answer = ask_local_model("What is diabetes?")
    print(answer)
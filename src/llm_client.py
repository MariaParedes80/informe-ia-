import httpx
import ollama


def consultar_llm(prompt, model_name="llama3.2:3b"):
    """Se conecta de forma resiliente con el cliente local de Ollama."""
    try:
        response = ollama.chat(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
        )
        return response["message"]["content"]
    except httpx.ConnectError:
        raise ConnectionError(
            "Ollama no responde. Inicie la app de Ollama en su equipo o corra 'ollama serve'."
        )
    except ollama.ResponseError as e:
        if "not found" in str(e).lower():
            raise FileNotFoundError(
                f"El modelo '{model_name}' no está instalado. Ejecute en su terminal: ollama pull {model_name}"
            )
        raise Exception(f"Error interno en Ollama: {e}")
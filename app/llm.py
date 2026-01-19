import requests

# URL for the Ollama LLM service
# 'ollama' is the service name from docker-compose
# 11434 is the port exposed by the Ollama container
OLLAMA_URL = "http://ollama:11434/api/generate"

"""
    This function sends a prompt to the Ollama LLM service and returns the generated response.

    Args:
        prompt (str): The text prompt to send to the model.
        model (str): The name of the model to use (default is "llama3").

    Returns:
        str: The generated text from the LLM.
    """
def generate_text(prompt: str, model: str = "llama3") -> str:
    # Make a POST request to the Ollama API with JSON payload
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": model,     # Specify which LLM model to use
            "prompt": prompt,   # The prompt text to generate from
            "stream": False     # Whether to stream output incrementally (False = wait for full response)
        },
        timeout=60  # Timeout in seconds for the HTTP request
    )

    # Raise an error if the HTTP request returned a non-2xx status code
    # This ensures any API failure is caught immediately
    response.raise_for_status()

    # Parse the JSON response returned by Ollama
    data = response.json()

    # Return only the 'response' field containing the generated text
    return data["response"]
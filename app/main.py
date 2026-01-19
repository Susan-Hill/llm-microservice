from fastapi import FastAPI
from pydantic import BaseModel

from app.llm import generate_text

# Main application object that routes and settings are attached to
app = FastAPI(title="LLM Microservice")

# Define a Pydantic model for the POST request payload to /generate
# This ensures the request has the correct structure and data types
class PromptRequest(BaseModel):
    prompt: str                 # The prompt string to send to the LLM

# Health check endpoint
# Simple GET endpoint to verify the API is running
@app.get("/health")
def health():
    return {"status": "ok"}     # Returns JSON indicating the service is healthy

# LLM text generation endpoint
# POST endpoint that accepts a JSON payload with a prompt
@app.post("/generate")
def generate(payload: PromptRequest):
    # Call the generate_text function (from app/llm.py) passing the prompt
    # This function handles communicating with the Ollama container
    output = generate_text(payload.prompt)

    # Return the LLM's response as JSON
    return {"response": output}
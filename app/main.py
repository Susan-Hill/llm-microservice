import logging
from fastapi import FastAPI, Request
from pydantic import BaseModel
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from starlette.responses import JSONResponse
from requests.exceptions import RequestException, Timeout

from app.llm import generate_text

# ============================
# Logging setup
# ============================

# Log info-level messages to stdout
logger = logging.getLogger("llm_microservice")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

# ============================
# FastAPI app setup
# ============================

# Main application object that routes and settings are attached to
app = FastAPI(title="LLM Microservice")

# ============================
# Rate limiter setup (SlowAPI)
# ============================

# Initialize Limiter (5 requests per minute per IP)
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# Exception handler for rate limit errors
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ==========================
# Pydantic models
# ==========================

# Define a Pydantic model for the POST request payload to /generate
# This ensures the request has the correct structure and data types
class PromptRequest(BaseModel):
    prompt: str                 # The prompt string to send to the LLM

# ==========================
# Endpoints
# ==========================

# Health check endpoint
# Simple GET endpoint to verify the API is running
@app.get("/health")
def health():
    return {"status": "ok"}     # Returns JSON indicating the service is healthy

# LLM text generation endpoint
# POST endpoint that accepts a JSON payload with a prompt
@app.post("/generate")
@limiter.limit("5/minute")      # Rate limit decorator applied
def generate(payload: PromptRequest, request: Request):
    client_ip = request.client.host
    prompt_text = payload.prompt

    # Log incoming request
    logger.info(f"Received prompt from {client_ip}: {prompt_text}")
    try:
        # Call the generate_text function (from app/llm.py) passing the prompt
        # This function handles communicating with the Ollama container
        output = generate_text(payload.prompt)

        # Log first 100 chars of response for debugging
        logger.info(f"Response to {client_ip} (first 100 chars): {output[:100]}")

        # Return the LLM's response as JSON
        return {"response": output}
    except Timeout:
        # Catch timeout
        logger.error("LLM request timed out.")
        return JSONResponse(
            content={"error": "LLM service timed out, please try again later."},
            status_code=503
        )
    except RequestException as e:
        # Catch other request-related exceptions
        logger.error(f"LLM request failed: {e}")
        return JSONResponse(
            content={"error": "LLM service unavailable, please try again later."},
            status_code=503
        )
    except Exception as e:
        # Catch-all for unexpected errors
        logger.exception("Unexpected error in /generate")
        return JSONResponse(
            content={"error": "Internal server error"},
            status_code=500
        )
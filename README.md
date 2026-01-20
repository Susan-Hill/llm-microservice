# FastAPI LLM Microservice

A **containerized FastAPI microservice** that integrates with an LLM (Llama3 via Ollama) for text generation.  
This project demonstrates deploying an AI service with **API endpoints, rate limiting, logging, and error handling**, fully containerized with Docker.

---

## Features

- FastAPI service with `/health` and `/generate` endpoints  
- Integration with Llama3 via Ollama API  
- **Rate limiting** using `slowapi` to prevent API abuse  
- **Structured logging** for requests and responses  
- **Timeout and error handling** to gracefully handle slow LLM responses  
- Fully containerized with Docker & Docker Compose  

---

## Getting Started

### Prerequisites
- [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/) installed  
- Ollama installed and running (inside container)  

### Installation

1. Clone this repository:

```bash
git clone https://github.com/<your-username>/llm-microservice.git
cd llm-microservice
```

2. Build and start the containers:
```
docker compose up --build
```
This will start two containers:
1. api – the FastAPI microservice
2. ollama – the LLM service (running Llama3)

---
## Usage

### Health Check
```
curl http://localhost:8000/health
```

Response:
```
{"status": "ok"}
```
### Generate Text
```
curl -X POST http://localhost:8000/generate \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Hello, FastAPI!"}'
```

Response:
```
{
  "response": "Hello there! I'm excited to help you with your FastAPI questions and projects."
}
```

Note: If the LLM is still processing a previous request or is slow (CPU-only), you may receive an error:
```
{"error": "LLM service timed out, please try again later."}
```

---
## Rate Limiting

- Default rate limit: 5 requests per minute per IP

- Requests exceeding the limit will return a 503 timed out response.

- Error handling ensures the service does not crash on timeouts.

---
## Logging

- Requests and responses are logged with timestamp and truncated response previews.

- Logs can be viewed in real-time:
```
docker compose logs -f api
```
---
## Known Limitations

- CPU-only LLM is slow; large prompts may hit timeouts

- Rate limiting is basic (per IP) and may need tuning for production

- GPU acceleration is recommended for production workloads

---
## Development Notes

- Python 3.11 slim used for minimal container size

- Dependencies listed in requirements.txt

- Fully containerized – no virtual environments needed

---
## License

MIT License © Susan Hill
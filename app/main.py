from fastapi import FastAPI

app = FastAPI(title="LLM Microservice")

@app.get("/health")
def health():
    return {"status": "ok"}
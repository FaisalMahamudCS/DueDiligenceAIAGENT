from fastapi import FastAPI
from src.api.routes import router
from src.utils.constants import API_PREFIX

app = FastAPI(title="Questionnaire Agent API")

# Include API routes
app.include_router(router, prefix=API_PREFIX)


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import chat, reservations
from app.models.schemas import HealthResponse

app = FastAPI(title="Chatbot Turismo API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api/v1", tags=["Chat"])
app.include_router(reservations.router, prefix="/api/v1", tags=["Reservations"])


@app.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(status="ok", version="1.0.0")

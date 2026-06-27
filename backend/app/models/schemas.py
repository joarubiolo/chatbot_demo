from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


class ReservationCreate(BaseModel):
    client_name: str
    client_email: str
    client_phone: str
    service: str
    date: str
    participants: int
    notes: str = ""


class ReservationResponse(BaseModel):
    id: str
    client_name: str
    client_email: str
    client_phone: str
    service: str
    date: str
    participants: int
    notes: str
    status: str
    created_at: str


class HealthResponse(BaseModel):
    status: str
    version: str

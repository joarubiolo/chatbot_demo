from fastapi import APIRouter, HTTPException
from app.models.schemas import ReservationCreate, ReservationResponse

router = APIRouter()

# Simula almacenamiento en memoria hasta conectar Supabase
_reservations: list[dict] = []
_id_counter = 0


@router.post("/reservations", response_model=ReservationResponse)
def create_reservation(data: ReservationCreate):
    global _id_counter
    _id_counter += 1
    reservation = {
        "id": str(_id_counter),
        "client_name": data.client_name,
        "client_email": data.client_email,
        "client_phone": data.client_phone,
        "service": data.service,
        "date": data.date,
        "participants": data.participants,
        "notes": data.notes,
        "status": "pending",
        "created_at": "",
    }
    _reservations.append(reservation)
    return reservation


@router.get("/reservations", response_model=list[ReservationResponse])
def list_reservations():
    return _reservations


@router.get("/reservations/{reservation_id}", response_model=ReservationResponse)
def get_reservation(reservation_id: str):
    for r in _reservations:
        if r["id"] == reservation_id:
            return r
    raise HTTPException(status_code=404, detail="Reserva no encontrada")


@router.patch("/reservations/{reservation_id}/cancel")
def cancel_reservation(reservation_id: str):
    for r in _reservations:
        if r["id"] == reservation_id:
            r["status"] = "cancelled"
            return {"detail": "Reserva cancelada"}
    raise HTTPException(status_code=404, detail="Reserva no encontrada")

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
from cors_config import add_cors

import random

app = FastAPI(title="Booking API", description="A simple API for booking appointments")
add_cors(app)


class BookingRequest(BaseModel):
    name: str
    phone: str

class BookingResponse(BaseModel):
    booking_id: str
    name: str
    phone: str
    appointment_date: str
    status: str
    message: str

@app.post("/book", response_model=BookingResponse)
async def create_booking(booking: BookingRequest):
    # Validate inputs
    if not booking.name:
        raise HTTPException(status_code=400, detail="Name is required")
    
    if not booking.phone:
        raise HTTPException(status_code=400, detail="Phone number is required")
    
    # Generate a random booking ID
    booking_id = f"BK-{random.randint(10000, 99999)}"
    
    # Generate a random appointment date (between tomorrow and next week)
    days_ahead = random.randint(1, 7)
    appointment_time = random.choice(['09:00', '10:30', '13:00', '14:30', '16:00'])
    appointment_date = (datetime.now() + timedelta(days=days_ahead)).strftime(f"%Y-%m-%d {appointment_time}")
    
    # Create response
    return BookingResponse(
        booking_id=booking_id,
        name=booking.name,
        phone=booking.phone,
        appointment_date=appointment_date,
        status="CONFIRMED",
        message=f"Thank you {booking.name}! Your appointment has been booked successfully."
    )

@app.get("/")
async def root():
    return {"message": "Welcome to the Booking API. Use /book endpoint to make a reservation."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

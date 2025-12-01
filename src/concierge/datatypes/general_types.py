from pydantic import BaseModel

class UserProfile(BaseModel):
    user_id: str
    name: str
    email: str
    phone: str
    
    

class OrderDetails(BaseModel):
    order_id: str
    user_id: str
    items: list[str]
    total_amount: float
    
    
class AppointmentInfo(BaseModel):
    appointment_id: str
    user_id: str
    date: str
    time: str
    location: str
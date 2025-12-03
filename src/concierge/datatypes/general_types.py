from pydantic import BaseModel, Field


class UserProfile(BaseModel):
    """User profile information."""

    user_id: str
    name: str
    email: str
    phone: str


class OrderItem(BaseModel):
    """Individual item in an order."""

    product_id: str
    name: str
    quantity: int
    price: float


class OrderDetails(BaseModel):
    """Complete order details."""

    order_id: str
    user_id: str
    items: list[OrderItem]
    total_amount: float
    status: str = Field(description="Order status: pending, processing, shipped, delivered, cancelled")
    created_at: str
    updated_at: str


class AppointmentInfo(BaseModel):
    """Appointment information."""

    appointment_id: str
    user_email: str
    user_phone: str
    date: str = Field(description="Date in YYYY-MM-DD format")
    time: str = Field(description="Time in HH:MM format")
    service_type: str
    status: str = Field(description="Appointment status: scheduled, confirmed, cancelled, completed")
    created_at: str


class Product(BaseModel):
    """Product information."""

    product_id: str
    name: str
    description: str
    price: float
    category: str
    in_stock: bool
    features: list[str]


class PolicyDocument(BaseModel):
    """Policy or service document."""

    doc_id: str
    title: str
    content: str
    category: str = Field(description="Category: shipping, returns, warranty, privacy, terms")
    keywords: list[str]

from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class BottleMaterial(str, Enum):
    glass = "vidrio"
    plastic = "plastico"


class OrderStatus(str, Enum):
    pending = "pendiente"
    paid = "pagada"
    shipped = "enviada"
    delivered = "entregada"
    cancelled = "cancelada"
    paid_display = "Pagado"
    fulfilled_display = "Surtido"
    cancelled_display = "Cancelado"


class Product(BaseModel):
    id: Optional[str] = None
    name: str = Field(min_length=2, max_length=120)
    description: str = Field(min_length=5, max_length=500)
    material: BottleMaterial
    capacity_ml: int = Field(gt=0)
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
    image_url: Optional[str] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class Customer(BaseModel):
    id: Optional[str] = None
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    phone: str = Field(min_length=7, max_length=30)
    address: str = Field(min_length=5, max_length=250)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class OrderItem(BaseModel):
    product_id: str
    product_name: str
    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0)
    subtotal: float = Field(gt=0)


class Order(BaseModel):
    id: Optional[str] = None
    customer_id: str
    items: list[OrderItem]
    status: OrderStatus = OrderStatus.pending
    total: float = Field(gt=0)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)

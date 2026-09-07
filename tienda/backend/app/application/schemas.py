from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from app.domain.entities import BottleMaterial, OrderItem, OrderStatus


class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    description: str = Field(min_length=5, max_length=500)
    material: BottleMaterial
    capacity_ml: int = Field(gt=0)
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
    image_url: Optional[str] = None
    is_active: bool = True


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=120)
    description: Optional[str] = Field(default=None, min_length=5, max_length=500)
    material: Optional[BottleMaterial] = None
    capacity_ml: Optional[int] = Field(default=None, gt=0)
    price: Optional[float] = Field(default=None, gt=0)
    stock: Optional[int] = Field(default=None, ge=0)
    image_url: Optional[str] = None
    is_active: Optional[bool] = None


class CustomerCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    phone: str = Field(min_length=7, max_length=30)
    address: str = Field(min_length=5, max_length=250)


class CustomerUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=120)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(default=None, min_length=7, max_length=30)
    address: Optional[str] = Field(default=None, min_length=5, max_length=250)


class OrderCreateItem(BaseModel):
    product_id: str
    quantity: int = Field(gt=0)


class OrderCreate(BaseModel):
    customer_id: str
    items: list[OrderCreateItem] = Field(min_length=1)


class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None


class ProductResponse(ProductCreate):
    id: str


class CustomerResponse(CustomerCreate):
    id: str
    created_at: datetime
    updated_at: datetime


class OrderResponse(BaseModel):
    id: str
    customer_id: str
    items: list[OrderItem]
    status: OrderStatus
    total: float
    created_at: datetime
    updated_at: datetime

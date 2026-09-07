from fastapi import APIRouter, Depends, Response, status

from app.api.dependencies import get_customer_use_cases, get_order_use_cases, get_product_use_cases
from app.application.schemas import CustomerCreate, CustomerResponse, CustomerUpdate, OrderCreate, OrderResponse, OrderUpdate, ProductCreate, ProductResponse, ProductUpdate
from app.application.use_cases import CustomerUseCases, OrderUseCases, ProductUseCases

router = APIRouter(prefix="/api")


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/products", response_model=list[ProductResponse])
async def list_products(use_cases: ProductUseCases = Depends(get_product_use_cases)):
    return await use_cases.list()


@router.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(data: ProductCreate, use_cases: ProductUseCases = Depends(get_product_use_cases)):
    return await use_cases.create(data)


@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str, use_cases: ProductUseCases = Depends(get_product_use_cases)):
    return await use_cases.get(product_id)


@router.patch("/products/{product_id}", response_model=ProductResponse)
async def update_product(product_id: str, data: ProductUpdate, use_cases: ProductUseCases = Depends(get_product_use_cases)):
    return await use_cases.update(product_id, data)


@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: str, use_cases: ProductUseCases = Depends(get_product_use_cases)):
    await use_cases.delete(product_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/customers", response_model=list[CustomerResponse])
async def list_customers(use_cases: CustomerUseCases = Depends(get_customer_use_cases)):
    return await use_cases.list()


@router.get("/clients", response_model=list[CustomerResponse])
async def list_clients(use_cases: CustomerUseCases = Depends(get_customer_use_cases)):
    return await use_cases.list()


@router.post("/customers", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
async def create_customer(data: CustomerCreate, use_cases: CustomerUseCases = Depends(get_customer_use_cases)):
    return await use_cases.create(data)


@router.get("/customers/{customer_id}", response_model=CustomerResponse)
async def get_customer(customer_id: str, use_cases: CustomerUseCases = Depends(get_customer_use_cases)):
    return await use_cases.get(customer_id)


@router.patch("/customers/{customer_id}", response_model=CustomerResponse)
async def update_customer(customer_id: str, data: CustomerUpdate, use_cases: CustomerUseCases = Depends(get_customer_use_cases)):
    return await use_cases.update(customer_id, data)


@router.delete("/customers/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(customer_id: str, use_cases: CustomerUseCases = Depends(get_customer_use_cases)):
    await use_cases.delete(customer_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/orders", response_model=list[OrderResponse])
async def list_orders(use_cases: OrderUseCases = Depends(get_order_use_cases)):
    return await use_cases.list()


@router.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(data: OrderCreate, use_cases: OrderUseCases = Depends(get_order_use_cases)):
    return await use_cases.create(data)


@router.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(order_id: str, use_cases: OrderUseCases = Depends(get_order_use_cases)):
    return await use_cases.get(order_id)


@router.patch("/orders/{order_id}", response_model=OrderResponse)
async def update_order(order_id: str, data: OrderUpdate, use_cases: OrderUseCases = Depends(get_order_use_cases)):
    return await use_cases.update(order_id, data)


@router.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: str, use_cases: OrderUseCases = Depends(get_order_use_cases)):
    await use_cases.delete(order_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

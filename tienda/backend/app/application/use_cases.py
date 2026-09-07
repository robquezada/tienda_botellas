from fastapi import HTTPException, status

from app.application.repositories import CustomerRepository, OrderRepository, ProductRepository
from app.application.schemas import CustomerCreate, CustomerUpdate, OrderCreate, OrderUpdate, ProductCreate, ProductUpdate
from app.domain.entities import Customer, Order, OrderItem, Product


class ProductUseCases:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    async def list(self) -> list[Product]:
        return await self.repository.list()

    async def get(self, product_id: str) -> Product:
        product = await self.repository.get(product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
        return product

    async def create(self, data: ProductCreate) -> Product:
        return await self.repository.create(Product(**data.model_dump()))

    async def update(self, product_id: str, data: ProductUpdate) -> Product:
        product = await self.repository.update(product_id, data)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
        return product

    async def delete(self, product_id: str) -> None:
        if not await self.repository.delete(product_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")


class CustomerUseCases:
    def __init__(self, repository: CustomerRepository):
        self.repository = repository

    async def list(self) -> list[Customer]:
        return await self.repository.list()

    async def get(self, customer_id: str) -> Customer:
        customer = await self.repository.get(customer_id)
        if not customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
        return customer

    async def create(self, data: CustomerCreate) -> Customer:
        return await self.repository.create(Customer(**data.model_dump()))

    async def update(self, customer_id: str, data: CustomerUpdate) -> Customer:
        customer = await self.repository.update(customer_id, data)
        if not customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
        return customer

    async def delete(self, customer_id: str) -> None:
        if not await self.repository.delete(customer_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")


class OrderUseCases:
    def __init__(self, orders: OrderRepository, products: ProductRepository, customers: CustomerRepository):
        self.orders = orders
        self.products = products
        self.customers = customers

    async def list(self) -> list[Order]:
        return await self.orders.list()

    async def get(self, order_id: str) -> Order:
        order = await self.orders.get(order_id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orden no encontrada")
        return order

    async def create(self, data: OrderCreate) -> Order:
        if not await self.customers.get(data.customer_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")

        items: list[OrderItem] = []
        for item in data.items:
            product = await self.products.get(item.product_id)
            if not product or not product.is_active:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Producto {item.product_id} no encontrado")
            if product.stock < item.quantity:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Stock insuficiente para {product.name}")
            subtotal = round(product.price * item.quantity, 2)
            items.append(OrderItem(product_id=item.product_id, product_name=product.name, quantity=item.quantity, unit_price=product.price, subtotal=subtotal))

        total = round(sum(item.subtotal for item in items), 2)
        return await self.orders.create(Order(customer_id=data.customer_id, items=items, total=total))

    async def update(self, order_id: str, data: OrderUpdate) -> Order:
        order = await self.orders.update_status(order_id, data.status.value) if data.status else await self.orders.get(order_id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orden no encontrada")
        return order

    async def delete(self, order_id: str) -> None:
        if not await self.orders.delete(order_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orden no encontrada")

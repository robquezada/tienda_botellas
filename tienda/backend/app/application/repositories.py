from abc import ABC, abstractmethod

from app.application.schemas import CustomerUpdate, ProductUpdate
from app.domain.entities import Customer, Order, Product


class ProductRepository(ABC):
    @abstractmethod
    async def list(self) -> list[Product]: ...

    @abstractmethod
    async def get(self, product_id: str) -> Product | None: ...

    @abstractmethod
    async def create(self, product: Product) -> Product: ...

    @abstractmethod
    async def update(self, product_id: str, data: ProductUpdate) -> Product | None: ...

    @abstractmethod
    async def delete(self, product_id: str) -> bool: ...


class CustomerRepository(ABC):
    @abstractmethod
    async def list(self) -> list[Customer]: ...

    @abstractmethod
    async def get(self, customer_id: str) -> Customer | None: ...

    @abstractmethod
    async def create(self, customer: Customer) -> Customer: ...

    @abstractmethod
    async def update(self, customer_id: str, data: CustomerUpdate) -> Customer | None: ...

    @abstractmethod
    async def delete(self, customer_id: str) -> bool: ...


class OrderRepository(ABC):
    @abstractmethod
    async def list(self) -> list[Order]: ...

    @abstractmethod
    async def get(self, order_id: str) -> Order | None: ...

    @abstractmethod
    async def create(self, order: Order) -> Order: ...

    @abstractmethod
    async def update_status(self, order_id: str, status: str) -> Order | None: ...

    @abstractmethod
    async def delete(self, order_id: str) -> bool: ...

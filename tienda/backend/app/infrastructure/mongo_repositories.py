from datetime import datetime, timezone
from typing import Any

from bson import ObjectId
from bson.errors import InvalidId
from pymongo import ReturnDocument

from app.application.schemas import CustomerUpdate, ProductUpdate
from app.domain.entities import Customer, Order, Product
from app.infrastructure.database import get_database


def _id_filter(entity_id: str) -> dict[str, ObjectId] | None:
    try:
        return {"_id": ObjectId(entity_id)}
    except InvalidId:
        return None


def _serialize(model: Product | Customer | Order) -> dict[str, Any]:
    data = model.model_dump(exclude={"id"})
    return data


def _with_id(document: dict[str, Any] | None) -> dict[str, Any] | None:
    if not document:
        return None
    document["id"] = str(document.pop("_id"))
    return document


class MongoProductRepository:
    @property
    def collection(self):
        return get_database().products

    async def list(self) -> list[Product]:
        docs = await self.collection.find().sort("created_at", -1).to_list(200)
        return [Product(**_with_id(doc)) for doc in docs]

    async def get(self, product_id: str) -> Product | None:
        query = _id_filter(product_id)
        if not query:
            return None
        return Product(**doc) if (doc := _with_id(await self.collection.find_one(query))) else None

    async def create(self, product: Product) -> Product:
        result = await self.collection.insert_one(_serialize(product))
        product.id = str(result.inserted_id)
        return product

    async def update(self, product_id: str, data: ProductUpdate) -> Product | None:
        query = _id_filter(product_id)
        if not query:
            return None
        payload = data.model_dump(exclude_unset=True)
        payload["updated_at"] = datetime.now(timezone.utc)
        doc = await self.collection.find_one_and_update(query, {"$set": payload}, return_document=ReturnDocument.AFTER)
        return Product(**doc) if (doc := _with_id(doc)) else None

    async def delete(self, product_id: str) -> bool:
        query = _id_filter(product_id)
        return bool(query and (await self.collection.delete_one(query)).deleted_count)


class MongoCustomerRepository:
    @property
    def collection(self):
        return get_database().customers

    async def list(self) -> list[Customer]:
        docs = await self.collection.find().sort("created_at", -1).to_list(200)
        return [Customer(**_with_id(doc)) for doc in docs]

    async def get(self, customer_id: str) -> Customer | None:
        query = _id_filter(customer_id)
        if not query:
            return None
        return Customer(**doc) if (doc := _with_id(await self.collection.find_one(query))) else None

    async def create(self, customer: Customer) -> Customer:
        result = await self.collection.insert_one(_serialize(customer))
        customer.id = str(result.inserted_id)
        return customer

    async def update(self, customer_id: str, data: CustomerUpdate) -> Customer | None:
        query = _id_filter(customer_id)
        if not query:
            return None
        payload = data.model_dump(exclude_unset=True)
        payload["updated_at"] = datetime.now(timezone.utc)
        doc = await self.collection.find_one_and_update(query, {"$set": payload}, return_document=ReturnDocument.AFTER)
        return Customer(**doc) if (doc := _with_id(doc)) else None

    async def delete(self, customer_id: str) -> bool:
        query = _id_filter(customer_id)
        return bool(query and (await self.collection.delete_one(query)).deleted_count)


class MongoOrderRepository:
    @property
    def collection(self):
        return get_database().orders

    async def list(self) -> list[Order]:
        docs = await self.collection.find().sort("created_at", -1).to_list(200)
        return [Order(**_with_id(doc)) for doc in docs]

    async def get(self, order_id: str) -> Order | None:
        query = _id_filter(order_id)
        if not query:
            return None
        return Order(**doc) if (doc := _with_id(await self.collection.find_one(query))) else None

    async def create(self, order: Order) -> Order:
        result = await self.collection.insert_one(_serialize(order))
        order.id = str(result.inserted_id)
        return order

    async def update_status(self, order_id: str, status: str) -> Order | None:
        query = _id_filter(order_id)
        if not query:
            return None
        doc = await self.collection.find_one_and_update(
            query,
            {"$set": {"status": status, "updated_at": datetime.now(timezone.utc)}},
            return_document=ReturnDocument.AFTER,
        )
        return Order(**doc) if (doc := _with_id(doc)) else None

    async def delete(self, order_id: str) -> bool:
        query = _id_filter(order_id)
        return bool(query and (await self.collection.delete_one(query)).deleted_count)

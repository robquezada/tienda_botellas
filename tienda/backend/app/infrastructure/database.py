from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.infrastructure.config import get_settings


client: AsyncIOMotorClient | None = None


def get_database() -> AsyncIOMotorDatabase:
    if client is None:
        raise RuntimeError("La base de datos no esta inicializada")
    settings = get_settings()
    return client[settings.mongodb_db_name]


async def connect_database() -> None:
    global client
    settings = get_settings()
    client = AsyncIOMotorClient(settings.mongodb_uri)
    database = client[settings.mongodb_db_name]
    await database.products.create_index("name")
    await database.products.create_index("material")
    await database.customers.create_index("email", unique=True)
    await database.orders.create_index("customer_id")


async def close_database() -> None:
    global client
    if client:
        client.close()
        client = None

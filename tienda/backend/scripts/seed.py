import asyncio
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.domain.entities import BottleMaterial, Product
from app.infrastructure.database import close_database, connect_database, get_database


PRODUCTS = [
    Product(name="Botella Ámbar Premium", description="Botella de vidrio ámbar para bebidas artesanales y kombucha.", material=BottleMaterial.glass, capacity_ml=500, price=2.75, stock=180, image_url="https://images.unsplash.com/photo-1602143407151-7111542de6e8?auto=format&fit=crop&w=900&q=80"),
    Product(name="PET Cristal Eco", description="Botella plástica ligera y reciclable para agua y jugos.", material=BottleMaterial.plastic, capacity_ml=1000, price=0.85, stock=900, image_url="https://images.unsplash.com/photo-1605405363458-2d028ed8a588?auto=format&fit=crop&w=900&q=80"),
    Product(name="Vidrio Swing Top", description="Botella reutilizable con cierre hermético para productos gourmet.", material=BottleMaterial.glass, capacity_ml=750, price=4.9, stock=95, image_url="https://images.unsplash.com/photo-1523362628745-0c100150b504?auto=format&fit=crop&w=900&q=80"),
]


async def main() -> None:
    await connect_database()
    database = get_database()
    if await database.products.count_documents({}) == 0:
        await database.products.insert_many([product.model_dump(exclude={"id"}) for product in PRODUCTS])
    await close_database()


if __name__ == "__main__":
    asyncio.run(main())

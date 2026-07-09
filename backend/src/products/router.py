from http.client import HTTPException

from fastapi import APIRouter

from ..database import DbSession

from ..products.service import fetch_all_products, fetch_product_by_id
from ..products.schemas import ProductScheme
router = APIRouter(prefix="/products",
                   tags=["Products"]
                   )

@router.get("/", summary="Получить все товары", response_model=list[ProductScheme])
async def get_all_products(session: DbSession):
    result = await fetch_all_products(session)
    return result

@router.get("/{product_id}", summary="Получить товар по id", response_model=ProductScheme)
async def get_one_product(product_id:int, session: DbSession):
    result = await fetch_product_by_id(product_id, session)
    if result is None:
        raise HTTPException(status_code=404, detail="Товар не найден ")
    return result
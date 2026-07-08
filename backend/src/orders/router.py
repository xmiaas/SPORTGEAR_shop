from fastapi import APIRouter, HTTPException
from typing import List

from ..orders.service import add_to_cart, remove_from_cart, get_cart
from ..orders.schemas import ProductInfo,ProductReturn, CartItemsReturn
from ..auth.dependencies import CurrentUser
from ..database import DbSession
basketRouter = APIRouter(prefix="/basket", tags=["Basket"])


@basketRouter.post("/add", response_model=ProductReturn, status_code=201)
async def add_to_basket(product_from_user: ProductInfo,user:CurrentUser, session: DbSession):
    result = await add_to_cart(session,product_from_user, user)
    if result is None:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return result

@basketRouter.delete("/delete/{product_id}",status_code=200,response_model=ProductReturn)
async def remove_from_basket(product_id: int,user:CurrentUser, session: DbSession):
    result= await remove_from_cart(session, product_id, user)
    if result is None:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return result

@basketRouter.get("/get_cart", response_model=List[CartItemsReturn])
async def get_basket(user: CurrentUser, session: DbSession):
    return await get_cart(session, user)



from typing import List

from fastapi import APIRouter, HTTPException
from ..auth.dependencies import CurrentAdmin
from ..database import DbSession
from ..admin.shemas import CreateItemDepends, UpdateItemDepends, CreateItemResponse, UpdateItemResponse, CategoryName, CategoryResponse
from ..products.schemas import ProductScheme
from ..admin.service import (create_item, delete_item, update_pr,
                             get_cat_name, get_all_cat, fetch_all_products,
                             fetch_product_by_id, create_cat,
                             delete_cat)
adminRouter = APIRouter(prefix="/admin", tags=["Admin"])

@adminRouter.post("/create_item", status_code=201, response_model=CreateItemResponse) #тут полностью переделывать надо потому что изоражение надо отправлять
async def add_item(session: DbSession, admin: CurrentAdmin, item: CreateItemDepends):
    result = await create_item(item, session)
    if result is None:
        raise HTTPException(status_code=400)
    return result


@adminRouter.patch("/update_item/{item_id}", response_model=UpdateItemResponse)
async def update_item(session: DbSession, admin:CurrentAdmin, item: UpdateItemDepends, item_id: int):
    res = await update_pr(item, item_id,session)
    if res is None:
        raise HTTPException(status_code=400)
    return res

@adminRouter.delete("/delete_item/{item_id}")
async def delete_ite(session: DbSession, admin: CurrentAdmin, item_id: int):
    result = await delete_item(item_id, session)
    if result:
        return item_id
    else:
        raise HTTPException(status_code=404)


@adminRouter.post("/create_category", response_model=CategoryResponse)
async def create_category(cat: CategoryName, session: DbSession, admin: CurrentAdmin):
    return await create_cat(session, cat)

@adminRouter.delete("/delete_category/{delete_index}", response_model=CategoryResponse)
async def delete_category(delete_index: int, session: DbSession, admin: CurrentAdmin):
    res = await delete_cat(session,delete_index)
    if res:
        return delete_index
    else:
        raise HTTPException(status_code=404)
@adminRouter.get("/get_category/{cat_id}", response_model=CategoryResponse)
async def get_category(cat_id: int, session: DbSession, admin: CurrentAdmin):
    return await get_cat_name(session, cat_id)

@adminRouter.get("/get_all_categories/", response_model=List[CategoryResponse])
async def get_all_categoris(session: DbSession, admin: CurrentAdmin):
    return await get_all_cat(session)



@adminRouter.get("/", summary="Получить все товары", response_model=list[ProductScheme])
async def get_all_products(session: DbSession, admin: CurrentAdmin):
    result = await fetch_all_products(session)
    return result

@adminRouter.get("/{product_id}", summary="Получить товар по id", response_model=ProductScheme)
async def get_one_product(product_id:int, session: DbSession, admin: CurrentAdmin):
    result = await fetch_product_by_id(product_id, session)
    if result is None:
        raise HTTPException(status_code=404, detail="Товар не найден ")
    return result
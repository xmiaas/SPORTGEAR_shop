from typing import List

from fastapi import APIRouter, HTTPException
from ..auth.dependencies import CurrentAdmin
from ..database import DbSession
from ..admin.shemas import CreateItemDepends, UpdateItemDepends, CreateItemResponse, UpdateItemResponse, CategoryNameResponse

from ..admin.service import create_item, delete_item, update_item, get_cat_name, get_all_cat
adminRouter = APIRouter(prefix="/admin", tags=["Admin"])

@adminRouter.post("/create_item", status_code=201, response_model=CreateItemResponse) #тут полностью переделывать надо потому что изоражение надо отправлять
async def add_item(session: DbSession, admin: CurrentAdmin, item: CreateItemDepends):
    result = await create_item(item, session)
    if result is None:
        raise HTTPException(status_code=400)
    return result


@adminRouter.patch("/update_item/{item_id}", response_model=UpdateItemResponse)
async def update_item(session: DbSession, admin:CurrentAdmin, item: UpdateItemDepends, item_id: int):
    res = await update_item(session, admin, item, item_id)
    if res is None:
        raise HTTPException(status_code=400)

@adminRouter.delete("/delete_item/{item_id}")
async def delete_item(session: DbSession, admin: CurrentAdmin, item_id: int):
    result = await delete_item(session, admin, item_id)
    return item_id


@adminRouter.post("/create_category")
async def create_category(session: DbSession, admin: CurrentAdmin):
    pass


@adminRouter.get("/get_category/{cat_id}", response_model=CategoryNameResponse)
async def get_category(cat_id: int, session: DbSession, admin: CurrentAdmin):
    return await get_cat_name(session, cat_id)

@adminRouter.get("/get_all_categories/", response_model=List[CategoryNameResponse])
async def get_all_categoris(session: DbSession, admin: CurrentAdmin):
    return await get_all_cat(session)

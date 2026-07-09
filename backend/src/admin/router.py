from fastapi import APIRouter
from ..auth.dependencies import CurrentAdmin
from ..database import DbSession
from ..admin.shemas import CreateItemSchema, UpdateItemSchema
adminRouter = APIRouter(prefix="/admin", tags=["Admin"])

@adminRouter.post("/create_item")
async def add_item(session: DbSession, admin: CurrentAdmin, item: CreateItemSchema):
    pass

@adminRouter.patch("/update_item/{item_id}")
async def update_item(session: DbSession, admin:CurrentAdmin, item: UpdateItemSchema, item_id: int):
    pass

@adminRouter.delete("/delete_item/{item_id}")
async def delete_item(session: DbSession, admin: CurrentAdmin, item_id: int):
    pass

# @adminRouter.get("/get_items")
# async def get_items(session: DbSession, admin:CurrentAdmin):
#     pass

@adminRouter.post("/create_category")
async def create_category(session: DbSession, admin: CurrentAdmin):
    pass


@adminRouter.get("/get_category/{cat_id}")
async def get_category(cat_id: int, session: DbSession, admin: CurrentAdmin):
    pass

@adminRouter.get("/get_all_categories/")
async def get_all_categoris(session: DbSession, admin: CurrentAdmin):
    pass

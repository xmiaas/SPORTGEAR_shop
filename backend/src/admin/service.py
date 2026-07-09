from unicodedata import category

from ..admin.shemas import CreateItemSchema, UpdateItemSchema
from ..products.models import Products, Categories

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,delete


async def get_cat_id(session:AsyncSession,category_name:str):
    res = await  session.execute(select(Categories).where(Categories.name == category_name))
    category = res.scalar_one_or_none()
    if category is None:
        return None
    category_id = category.id
    return category_id

async def create_item(item: CreateItemSchema, session: AsyncSession):

    category_id = await get_cat_id(session, item.category)

    new_item = Products(**item.model_dump(exclude={"category"}))
    new_item.category_id = category_id



    session.add(new_item)
    await session.commit()
    await session.refresh(new_item)

    return new_item


async def update_item(item_update:UpdateItemSchema, item_id: int, session: AsyncSession):
    item = await session.get(Products, item_id)
    if not item:
         return None
    update_data = item_update.model_dump(exclude_unset=True)

    if "category" in update_data:
        category_name = update_data.pop("category")
        cat_id = await get_cat_id(session, category_name)
        if cat_id is None:
            return None
        item.category_id = cat_id

    for key, value in update_data.items():
        setattr(item, key,value)

    await session.commit()
    await session.refresh(item)

    return item

async def delete_item(item_id: int, session:AsyncSession):
    result = await session.execute(delete(Products).where(Products.id == item_id))

    if result.rowcount == 0:
        return False
    await session.commit()
    return True


async def get_cat_name(session: AsyncSession, cat_id: int):
    res = await session.get(Categories, cat_id)
    if res is None:
        return None
    return res.name

async def get_all_cat(session: AsyncSession):
    res = await session.execute(select(Categories))
    cat = res.scalars().all()
    names = [el.name for el in cat]
    return names


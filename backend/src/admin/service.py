from fastapi import UploadFile

from ..admin.shemas import CreateItemDepends, UpdateItemDepends, CategoryName
from ..products.models import Products, Categories

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,delete
from sqlalchemy.orm import selectinload

import os
import aiofiles.os

async def get_cat_id(session:AsyncSession,category_name:str):
    res = await  session.execute(select(Categories).where(Categories.name == category_name))
    category = res.scalar_one_or_none()
    if category is None:
        return None
    category_id = category.id
    return category_id

def get_dir(file_name):
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    PARENT_DIR = os.path.dirname(CURRENT_DIR)
    ROOT_DIR = os.path.dirname(PARENT_DIR)
    DIR = os.path.join(ROOT_DIR, "photos")
    return  os.path.join(DIR, file_name)

async def create_item(item: CreateItemDepends ,session: AsyncSession):

    category_id = await get_cat_id(session, item.category)
    if category_id is None:
        return None
    data_dict = vars(item).copy()
    data_dict.pop("category")
    data_dict.pop("photo")
    new_item = Products(**data_dict)
    new_item.category_id = category_id

    file =  item.photo
    if not file or not file.filename:
        return None

    RES_DIR = get_dir(file.filename)

    file_bytes = await file.read()

    async with aiofiles.open(RES_DIR, "wb") as f:
        await f.write(file_bytes)

    new_item.photo_link = file.filename


    session.add(new_item)
    await session.commit()
    await session.refresh(new_item)

    return new_item


async def update_pr(item_update:UpdateItemDepends, item_id: int, session: AsyncSession):
    item = await session.get(Products, item_id)
    if not item:
         return None
    update_data = item_update.to_dict()

    if "category" in update_data:
        category_name = update_data.pop("category")
        cat_id = await get_cat_id(session, category_name)
        if cat_id is None:
            return None
        item.category_id = cat_id

    if "photo" in update_data:
        file = update_data.pop("photo")

        RES_DIR = get_dir(file.filename)

        file_bytes = await file.read()

        async with aiofiles.open(RES_DIR, "wb") as f:
            await f.write(file_bytes)

        item.photo_link = file.filename
    for key, value in update_data.items():
        setattr(item, key,value)

    await session.commit()
    await session.refresh(item)

    return item

async def delete_item(item_id: int, session:AsyncSession):
    item = await session.get(Products, item_id)
    path = get_dir(item.photo_link)
    if await aiofiles.os.path.exists(path):
        await aiofiles.os.remove(path)
    result = await session.execute(delete(Products).where(Products.id == item_id))

    if result.rowcount == 0:
        return False
    await session.commit()
    return True


async def get_cat_name(session: AsyncSession, cat_id: int):
    res = await session.get(Categories, cat_id)
    if res is None:
        return None
    return res

async def get_all_cat(session: AsyncSession):
    res = await session.execute(select(Categories))
    cat = res.scalars().all()
    return cat


async def fetch_all_products(session: AsyncSession):
    result = await session.execute(select(Products)
                                   .options(selectinload(Products.category)))
    products = result.scalars().all()
    return products

async def fetch_product_by_id(pr_id: int, session: AsyncSession):
    result = await session.execute(select(Products)
                                   .where(Products.id==pr_id)
                                   .options(selectinload(Products.category)))
    product = result.scalar_one_or_none()
    return product


async def create_cat(session: AsyncSession, item: CategoryName):
    new_item = Categories()
    new_item.name = item.name
    session.add(new_item)
    await session.commit()
    await session.refresh(new_item)
    return new_item

async def delete_cat(session: AsyncSession, cat_id: int):
    result = await session.execute(delete(Categories).where(Categories.id == cat_id))
    if result.rowcount == 0:
        return False
    await session.commit()
    return True


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from ..products.models import Products

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
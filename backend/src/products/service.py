
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..products.models import Products

async def fetch_all_products(session: AsyncSession):
    result = await session.execute(select(Products))
    products = result.scalars().all()
    return products

async def fetch_product_by_id(pr_id: int, session: AsyncSession):
    result = await session.execute(select(Products).where(Products.id==pr_id))
    product = result.scalar_one_or_none()
    return product
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ..auth.dependencies import CurrentUser
from ..orders.schemas import ProductInfo, ProductReturn, CartItemsReturn
from ..products.models import Products
from ..orders.models import Cart

from typing import List

async def add_to_cart(session: AsyncSession, product_from_user: ProductInfo, user: CurrentUser) ->ProductReturn | None:
    product = await session.get(Products, product_from_user.id)
    if not product:
        return None

    user_id = user.id

    result = await session.execute(select(Cart).where(
        Cart.product_id==product_from_user.id,
        Cart.user_id == user.id
    ))

    user_products = result.scalar_one_or_none()
    if user_products is None:
        new_count = 1
        session.add(Cart(product_id=product_from_user.id, user_id=user_id, count=new_count))
    else:
        new_count = user_products.count + 1
        user_products.count = new_count
        # await session.execute(update(Cart)
        #                       .where(Cart.user_id == user_id,
        #                              Cart.product_id == product_from_user.id)
        #                       .values(count=new_count))


    await session.commit()

    return ProductReturn(id=product_from_user.id,count=new_count)



async def remove_from_cart(session: AsyncSession, product_id: int, user: CurrentUser):
    product = await session.get(Products, product_id)
    if not product:
        return None

    user_id = user.id

    result = await session.execute(select(Cart).where(
        Cart.product_id == product_id,
        Cart.user_id == user.id
    ))
    user_products = result.scalar_one_or_none()

    if user_products is None:
        return None
    elif user_products.count == 1:
        await session.delete(user_products)
        new_count = 0
    else:
        user_products.count -=1
        new_count = user_products.count

    await session.commit()

    return ProductReturn(id=product_id, count=new_count)


async def get_cart(session: AsyncSession, user:CurrentUser) -> List[CartItemsReturn]:
    user_id = user.id
    result = await session.execute(select(Cart)
                                   .where(Cart.user_id==user_id)
                                   .options(selectinload(Cart.products)
                                    .selectinload(Products.category)
                                    ))
    items = result.scalars().all()
    return [CartItemsReturn(id=item.products.id,
                            count=item.count,
                            productName=item.products.productName,
                            category=item.products.category.name,
                            description=item.products.description,
                            price=item.products.price,
                            photo_link=item.products.photo_link) for item in items]













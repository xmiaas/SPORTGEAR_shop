from fastapi import APIRouter

from ..auth.dependencies import CurrentUser
from ..database import DbSession
basketRouter = APIRouter(prefix="/basket", tags=["Basket"])


@basketRouter.get("/add")
async def add_to_basket( user:CurrentUser):
    return {"user": user}
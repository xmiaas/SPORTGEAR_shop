from fastapi import APIRouter
from ..auth.schemas import UserInCreate, UserInLogin, UserOutput

authRouter = APIRouter(prefix="/auth", tags=["Authorization and login"])

@authRouter.post("/login")
async def login(loginDetails: UserInLogin):
    return {"data":"login"}

@authRouter.post("/signup")
async def sign_up(loginDetails: UserInCreate):
    return {"data":UserOutput}
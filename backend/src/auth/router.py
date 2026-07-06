from fastapi import APIRouter
from ..auth.schemas import UserInCreate, UserInLogin, UserOutput, UserWithToken
from ..auth.service import login, sign_up

from ..database import DbSession

authRouter = APIRouter(prefix="/auth", tags=["Authorization and login"])

@authRouter.post("/login", status_code=200, response_model=UserWithToken)
async def login_r(loginDetails: UserInLogin, session: DbSession):
    try:
        return await login(session, loginDetails)
    except Exception as error:
        print(error)
        raise error


@authRouter.post("/signup", status_code=201, response_model=UserOutput)
async def sign_up_r(signUpDetails: UserInCreate, session: DbSession):
    try:
        return await sign_up(session, signUpDetails)
    except Exception as error:
        print(error)
        raise error

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, Union



from ..auth.service import AuthHandler, get_user_by_id
from ..database import DbSession
from ..auth.schemas import UserOutput


AUTH_PREFIX = "Bearer "

async def get_current_user(session: DbSession, authorization: Annotated[str | None, Header()]) ->UserOutput:
    auth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неверные данные аунтификации "
                                   )

    if not authorization:
        raise auth_exception

    if not authorization.startswith(AUTH_PREFIX):
        raise auth_exception

    payload = AuthHandler.decode_jwt(token=authorization[len(AUTH_PREFIX):])

    if payload and payload["user_id"]:
        user = await get_user_by_id(session, payload["user_id"])
        if user:
            return UserOutput(id=user.id,
                          user_name=user.user_name,
                          email=user.email
                          )
        else:
            raise auth_exception
    else:
        raise auth_exception

CurrentUser = Annotated[UserOutput,Depends(get_current_user)]
import time

from fastapi import HTTPException, status


from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..auth.models import User
from ..auth.schemas import UserInCreate

from ..config import settings

from bcrypt import checkpw, hashpw, gensalt

import jwt

#помощь с поролями

class HashHelper():
    @staticmethod
    def verify_password(plain_password:str, hash_password): #проверяет пороль от клиента с бд
        return checkpw(plain_password.encode("UTF-8"), hash_password.encode("UTF-8")) #нельзя через == так как используется соль при шифровании

    @staticmethod
    def get_password_hash(password: str): #хеширует пароль
        return hashpw(
            password.encode("UTF-8"),
            gensalt(rounds=12))


#РАБОТА С JWT

JWT_SECRET_KEY = settings.SECRET_KEY
JWT_ALG = settings.ALGORITHM
class AuthHandler():
    @staticmethod
    def sign_jwt(user_id:int, is_admin: bool): #генерация jwt токена на 15 минут
        payload = {
                "user_id": user_id,
                "expires": time.time()+ 900 #надо будет исправить
        }
        token = jwt.encode(payload,JWT_SECRET_KEY,JWT_ALG)
        return token

    @staticmethod
    def decode_jwt(token: str) -> dict: #декодирование токена
        try:
            decode_token = jwt.decode(token, JWT_SECRET_KEY,algorithms=[JWT_ALG])
            if decode_token["expires"] >= time.time():
                return decode_token
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Истекло время жизни")
        except:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Невалидный токен")




#РАБОТА С БД
async def create_user(user_data: UserInCreate, session: AsyncSession):
    new_user = User(**user_data.model_dump(exclude_none=True))

    session.add(new_user)
    await session.commit()
    await session.refresh(instance=new_user)
    return new_user

async def user_exist_by_email(session: AsyncSession, email: str) -> bool:
    result = await session.execute(select(User).where(User.email == email))
    user = result.scalar()
    return user is not None

async def get_user_by_email(session: AsyncSession, email: str):
    result = await session.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    return user

async def get_user_by_id(session: AsyncSession, id: int):
    return await session.get(User, id)






from pydantic import BaseModel, EmailStr, Field

class UserInCreate(BaseModel):
    user_name: str = Field(min_length=3, max_length=60)
    email: EmailStr = Field(max_length=100)
    password_hash: str


class UserOutput(BaseModel):
    id: int
    user_name: str = Field(min_length=3, max_length=60)
    email: EmailStr = Field(max_length=100)
    is_admin: bool | None = None

class UserInUpdate(BaseModel):
    user_name: str | None = Field(min_length=3, max_length=60, default=None)
    email: EmailStr | None = Field(max_length=100, default=None)
    password: str | None = None

class UserInLogin(BaseModel):
    email: EmailStr = Field(max_length=100)
    password: str

class UserWithToken(BaseModel):
    token:str


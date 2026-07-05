from ..database import Base
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import String, Boolean


class User(Base):
    __tablename__ = "users"
    user_name: Mapped[str] = mapped_column(String(60), unique=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, server_default="FALSE")
    
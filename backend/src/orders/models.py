from ..database import Base
from sqlalchemy.orm import Mapped,mapped_column, relationship
from sqlalchemy import String, Numeric, ForeignKey

class Cart(Base):
    __tablename__ = "cart"
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    count: Mapped[int]

    products = relationship("Products", back_populates="cart")
    user = relationship("User", back_populates="cart")
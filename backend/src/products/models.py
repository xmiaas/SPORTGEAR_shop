from ..database import Base
from typing import List
from sqlalchemy.orm import Mapped,mapped_column, relationship
from sqlalchemy import String, Numeric, ForeignKey

class Categories(Base):
    __tablename__ = "categories"
    name: Mapped[str] = mapped_column(String(60), unique=True)
    products:Mapped[List["Products"]] = relationship(back_populates="category")

class Products(Base):
    __tablename__ = "products"
    productName: Mapped[str] = mapped_column(String(60), unique=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped["Categories"] = relationship(back_populates="products")
    description: Mapped[str | None] = mapped_column(String(200))
    price: Mapped[float] = mapped_column(Numeric(precision=10, scale=2))
    photo_link: Mapped[str | None] = mapped_column(String(100))

    cart: Mapped[List["Cart"]] = relationship("Cart", back_populates="products")

    @property
    def get_cat_name(self):
        if self.category:
            return self.category.name
        return ""
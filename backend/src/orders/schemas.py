from pydantic import BaseModel, Field

class ProductInfo(BaseModel):
    id: int

class ProductReturn(ProductInfo):
    count:int

class CartItemsReturn(ProductReturn):
    productName: str = Field(min_length=3,max_length=60)
    category: str
    description: str | None = Field(max_length=200, default=None)
    price: int
    photo_link: str = Field(max_length=100)
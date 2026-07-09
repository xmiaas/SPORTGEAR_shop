from pydantic import BaseModel, Field

class CreateItemSchema(BaseModel):
    productName: str = Field(min_length=10, max_length=60)
    category: str = Field(max_length=60)
    description: str | None = Field(max_length=200)
    price: float = Field(ge=10)
    photo_link: str | None = Field(max_length=100)


class UpdateItemSchema(BaseModel):
    productName: str | None = Field(min_length=10, max_length=60, default=None)
    category: str | None = Field(max_length=60, default=None)
    description: str | None = Field(max_length=200, default=None)
    price: float | None = Field(ge=10, default=None)
    photo_link: str | None = Field(max_length=100, default=None)
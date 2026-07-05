from pydantic import BaseModel, Field, ConfigDict

class ProductScheme(BaseModel):
    id: int
    productName: str = Field(min_length=10, max_length=60)
    category_id: int
    description: str | None = Field(max_length=200)
    price: float = Field(ge=10)
    photo_link: str | None = Field(max_length=100)

    model_config = ConfigDict(from_attributes=True)

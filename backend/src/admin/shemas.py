from pydantic import BaseModel, Field
from fastapi import Form, Depends
from typing import Annotated
from fastapi import UploadFile, File

class CreateItemForm:
    def __init__(self,
                 productName: str = Form(min_length=3, max_length=60),
                 category: str = Form(max_length=60),
                 description: str | None = Form(max_length=200),
                 price: float = Form(ge=10),
                 photo: UploadFile = File()
                 ):
        self.productName = productName
        self.category = category
        self.description = description
        self.price = price
        self.photo = photo

CreateItemDepends = Annotated[CreateItemForm, Depends(CreateItemForm)]

class CreateItemResponse(BaseModel):
    id: int
    productName: str
    price: float



class UpdateItemForm:
    def __init__(self,
    productName: str | None = Form(min_length=10, max_length=60, default=None),
    category: str | None = Form(max_length=60, default=None),
    description: str | None = Form(max_length=200, default=None),
    price: float | None = Form(ge=10, default=None),
    photo: str | None = File(default=None)
                 ):
        self.productName = productName
        self.category = category
        self.description = description
        self.price = price
        self.photo = photo

    def to_dict(self):
        for key, value in self.__dict__.items():
            if value is None:
                self.__dict__.pop(key)


UpdateItemDepends = Annotated[UpdateItemForm, Depends(UpdateItemForm)]

class UpdateItemForm:
    def __init__(self,
    productName: str | None,
    category: str | None ,
    description: str | None ,
    price: float | None ,
    photo: str | None
                 ):
        self.productName = productName
        self.category = category
        self.description = description
        self.price = price
        self.photo = photo

    def to_dict(self):
        key_to_remove = [key for key, value in self.__dict__.items() if value is None]
        for key in key_to_remove:
            self.__dict__.pop(key)


class UpdateItemResponse(BaseModel):
    id: int
    productName: str
    price: float


class CategoryNameResponse:
    id: int
    name: str
from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional, Union


class UserInProduct(BaseModel):
    id: int
    first_name: str = "John"
    last_name: str = "Doe"
    email: EmailStr = "j_doe@gmail.com"
    activated: bool
    admin: bool

    class Config:
        orm_mode = True


class ProductBase(BaseModel):
    title: str = "product_1"
    description: str = "product_description"
    set_price: float = 1500.99
    storage: int = 5
    featured: bool = True
    hidden: bool = False


class ProductDisplay(ProductBase):
    id: int
    created_at: datetime
    updated_at: Union[datetime, None]
    # added_by: int
    user: UserInProduct

    class Config:
        orm_mode = True


class ProductDisplaySimple(ProductBase):
    id: int
    created_at: datetime
    updated_at: Union[datetime, None]

    class Config:
        orm_mode = True

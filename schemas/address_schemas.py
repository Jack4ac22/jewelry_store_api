from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional, Union
import enum
from schemas import personalized_enums


class UserInAddress(BaseModel):
    id: int
    first_name: str = "John"
    last_name: str = "Doe"
    email: EmailStr = "j_doe@gmail.com"
    activated: bool

    class Config:
        orm_mode = True


class AddressBase(BaseModel):
    # user_id: Optional[int]
    address_description: Optional[str]
    country: str
    state: str
    county: Optional[str]
    street_name: str
    number: str
    extra_details: Optional[str]
    active_address: bool


class AddressDisplay(BaseModel):
    id: int
    address_description: Union[str, None]
    country: str
    state: str
    county: Union[str, None]
    street_name: str
    number: str
    extra_details: Union[str, None]
    active_address: bool
    created_at: datetime
    updated_at: Union[datetime, None]
    user: UserInAddress

    class Config:
        orm_mode = True

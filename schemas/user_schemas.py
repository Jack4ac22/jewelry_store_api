from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional, Union
import enum
from schemas import personalized_enums


class UserBase(BaseModel):
    first_name: str = "John"
    last_name: str = "Doe"
    email: EmailStr = "j_doe@gmail.com"
    password: str = "die_hard"


class RequestPassword(BaseModel):
    email: EmailStr = "j_doe@gmail.com"


class PasswordReset(BaseModel):
    new_password: str = "New_Password"


class UserDisplay(BaseModel):
    id: int
    created_at: datetime
    updated_at: Union[datetime, None]
    activated: bool
    verified: bool

    class Config:
        orm_mode = True

from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional, Union
import enum
from schemas import personalized_enums


class UserBase(BaseModel):
    username: str = "username"
    password: str = "password"
    secret_password: str = "secret_password"
    email: EmailStr


class UserDisplay(BaseModel):
    id: int
    username: str = "username"
    email: EmailStr
    activated: bool
    created_at: datetime
    updated_at: datetime
    deleted: bool

    class Config:
        orm_mode = True

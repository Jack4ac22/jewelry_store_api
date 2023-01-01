# from datetime import datetime, date, time
# from pydantic import BaseModel, EmailStr
# from schemas import personalized_enums, user_schemas
# from typing import Optional
# import enum


# class UserInImage(BaseModel):
#     id: int
#     username: str

#     class Config:
#         orm_mode = True


# class PersonInImage(BaseModel):
#     id: int
#     first_name: str
#     last_name: str

#     class Config:
#         orm_mode = True


# class ImageUpload(BaseModel):
#     title: str = 'image'
#     description: str = 'image description'


# class ImageDisplay(ImageUpload):
#     id: str
#     path: str
#     person: PersonInImage
#     user_id: int

#     class Config:
#         orm_mode = True

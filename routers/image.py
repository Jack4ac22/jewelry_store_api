from db import db_image
from db.database import get_db
from fastapi import APIRouter, Depends, UploadFile, File
from schemas import image_schemas
from sqlalchemy.orm import Session
from utilities import jwt_manager
from typing import List


router = APIRouter(
    prefix='/image',
    tags=['image']
)


# @router.post('/{person_id}/{user_id}', response_model=image_schemas.ImageDisplay)
# def upload_image(request: image_schemas.ImageUpload, person_id: int, user_id: int, image: UploadFile = File(...), db: Session = Depends(get_db)):
#     return db_image.upload_new_image(request, db, person_id, user_id, image)


# @router.delete('/{image_id}')
# def delete_image(image_id: int, db: Session = Depends(get_db), user_id: int = Depends(jwt_manager.decode_token)):
#     return db_image.delete_an_image(db, user_id, image_id)


# @router.get("/p{p_id}",
#             response_model=List[image_schemas.ImageDisplay],
#             summary="Get the images that are related to a single product.")
# def get_product_images(p_id: int, db: Session = Depends(get_db)):
#     return db_image.get_a_product_images(db, p_id)

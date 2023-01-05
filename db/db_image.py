
from fastapi import Depends, HTTPException, Response, status, UploadFile, File
from schemas import image_schemas
from sqlalchemy.orm import Session
import os
import random
import shutil
import string


# def upload_new_image(request: image_schemas.ImageUpload, db: Session, person_id: int, user_id: int, image: UploadFile):
#     leters = string.ascii_letters
#     rand_str = ''.join(random.choice(leters) for i in range(6))
#     new = f"_{rand_str}."
#     filemame = new.join(image.filename.split('.', 1))
#     path = f"images/{filemame}"
#     with open(path, 'w+b') as buffer:
#         shutil.copyfileobj(image.file, buffer)
#     new_image = DbImage_Up(
#         title=request.title,
#         description=request.description,
#         path=path,
#         person_id=person_id,
#         user_id=user_id
#     )
#     db.add(new_image)
#     db.commit()
#     db.refresh(new_image)
#     return new_image


# def delete_an_image(db: Session, user_id: int, image_id: int):
#     targeted_image = db.query(DbImage_Up).filter(
#         DbImage_Up.id == image_id)
#     if not targeted_image.first():
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"No corresponding Image was found with ID: {image_id}, please verify the ID and try again."
#         )
#     file_path = targeted_image.first().__dict__['path']
#     print(file_path)
#     try:
#         os.remove(file_path)
#     except:
#         pass
#     deleted_image = targeted_image.first()
#     targeted_image.delete()
#     db.commit()
#     return deleted_image

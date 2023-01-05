from fastapi import APIRouter, Depends, status
from db.database import get_db
from schemas import user_schemas, other_schemas
from sqlalchemy.orm.session import Session
from db import db_user
from pydantic import EmailStr
from utilities import jwt_manager

router = APIRouter(
    prefix='/user',
    tags=['user']
)


@router.post("", response_model=user_schemas.UserDisplay, status_code=status.HTTP_201_CREATED)
def create_new_user(request: user_schemas.UserBase, db: Session = Depends(get_db)):
    return db_user.create_user(request, db)


@router.post("/activate/{token}", response_model=user_schemas.UserDisplay)
def validate_email(token: str, db: Session = Depends(get_db)):
    return db_user.validate_email_address_for_new_user(token, db)


@router.post("/request_password_reset")
def request_password_reset(request: user_schemas.RequestPassword, db: Session = Depends(get_db)):
    return db_user.reset_request(request, db)


@router.post("/reset_password/{token}", response_model=user_schemas.UserDisplay)
def reset_password(token: str, request: user_schemas.PasswordReset, db: Session = Depends(get_db)):
    return db_user.reset_password_for_user(token, request, db)


@router.post("/deactivate")
def deactivate_request(id: int = Depends(jwt_manager.decode_token_id), db: Session = Depends(get_db)):
    return db_user.request_deactivation(id, db)


@router.post("/deactivate/{token}", response_model=user_schemas.UserDisplay)
def deactivate_account(token: str, id: int = Depends(jwt_manager.decode_token_id), db: Session = Depends(get_db)):
    return db_user.deactivate(token, id, db)

# TODO: add end point to request a new validation if user did not recieve

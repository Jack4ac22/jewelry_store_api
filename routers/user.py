from fastapi import APIRouter, Depends
from db.database import get_db
from schemas import user_schemas, other_schemas
from sqlalchemy.orm.session import Session
from db import db_user
from pydantic import EmailStr

router = APIRouter(
    prefix='/user',
    tags=['user']
)


@router.post("", response_model=user_schemas.UserDisplay)
def create_new_user(request: user_schemas.UserBase, db: Session = Depends(get_db)):
    return db_user.create_user(request, db)


@router.get("/activate/{token}", response_model=user_schemas.UserDisplay)
def validate_email(token: str, db: Session = Depends(get_db)):
    return db_user.validate_email_address_for_new_user(token, db)


@router.post("/request_password_reset")
def request_password_reset(request: user_schemas.RequestPassword, db: Session = Depends(get_db)):
    return db_user.reset_request(request, db)


@router.post("/reset_password/{token}", response_model=user_schemas.UserDisplay)
def reset_password(token: str, request: user_schemas.PasswordReset, db: Session = Depends(get_db)):
    return db_user.reset_password_for_user(token, request, db)


# TODO:request deactivation

# TODO: deactivate the account

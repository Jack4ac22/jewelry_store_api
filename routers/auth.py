from db import models
from db.database import get_db
from fastapi import Depends, Response, status, APIRouter, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from utilities import hash_manager, jwt_manager
from schemas import other_schemas

router = APIRouter(
    prefix='/auth',
    tags=['authentication']
)

incorrectException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password ",
    headers={"WWW-Authenticate": "Bearer"}
)


@router.post('', status_code=status.HTTP_202_ACCEPTED, response_model=other_schemas.Token)
def auth_user(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    corresponding_user: models.DbUser = db.query(models.DbUser).filter(
        models.DbUser.email == user_credentials.username).first()

    if not corresponding_user:
        raise incorrectException

    pass_valid = hash_manager.verify_password(
        user_credentials.password, corresponding_user.password)

    if not pass_valid:
        raise incorrectException

    jwt = jwt_manager.generate_token(
        corresponding_user.id, corresponding_user.email, corresponding_user.activated)
    return jwt

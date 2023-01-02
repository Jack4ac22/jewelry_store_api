from sqlalchemy.orm.session import Session
from .models import DbUser
from fastapi import HTTPException, status

############################
### User's check methods ###
############################


def check_user_id(user_id: int, db: Session):
    user = db.query(DbUser).filter(DbUser.id == user_id)
    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No corresponding user was found with ID: {user_id}, please verify the ID and try again."
        )
    return user


def check_user_by_email(email_address: str, db: Session):
    user = db.query(DbUser).filter(DbUser.email == email_address)
    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No corresponding User were found with the given email address."
        )
    return user

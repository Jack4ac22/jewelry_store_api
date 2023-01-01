from sqlalchemy.orm.session import Session
from schemas import user_schemas, personalized_enums
from .models import DbUser
from utilities import hash_manager

# TODO: add verification for the email -- unique
# add the other methods...


def create_user(request: user_schemas.UserBase, db: Session):
    hashed_password = hash_manager.hash_pass(request.password)
    hashed_secret_password = hash_manager.hash_pass(request.secret_password)

    new_user = DbUser(
        username=request.username,
        password=hashed_password,
        secret_password=hashed_secret_password,
        email=request.email
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

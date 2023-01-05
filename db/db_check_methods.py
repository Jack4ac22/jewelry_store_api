from sqlalchemy.orm.session import Session
from .models import DbUser, DbAddress, DbProduct
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


def check_email_usage(email_address: str, db: Session):
    user = db.query(DbUser).filter(DbUser.email == email_address).first()
    if user:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"The email: '{email_address}' is already used.")


def check_admin_status(user_id: int, db: Session):
    return check_user_id(user_id, db).first().admin


def admin_only_method(user_id: int, db: Session):
    if not check_admin_status(user_id, db):
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="This method is not allowed."
        )
    return True


###############################
## address's checking methods##
###############################


def check_address_id(id: int, db: Session):
    targeted_address = db.query(DbAddress).filter(DbAddress.id == id)
    if not targeted_address.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No corresponding address was found with ID: {id}, please verify the ID and try again."
        )
    return targeted_address


###############################
## product's checking methods##
###############################


def check_product_id(id: int, db: Session):
    targeted_product = db.query(DbProduct).filter(DbProduct.id == id)
    if not targeted_product.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No corresponding product was found with ID: {id}, please verify the ID and try again."
        )
    return targeted_product

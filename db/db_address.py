from sqlalchemy.orm.session import Session
from schemas import address_schemas
from .models import DbAddress
from db import db_check_methods
from fastapi import HTTPException, status


####################
## database methods##
###################


def create_address(address_user_id: int, user_id: int, request: address_schemas.AddressBase, db: Session):
    if not db_check_methods.check_admin_status(user_id, db):
        new_address = DbAddress(user_id=user_id,
                                **request.dict())
    else:
        new_address = DbAddress(user_id=address_user_id,
                                **request.dict())
        db_check_methods.check_user_id(address_user_id, db)
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    return new_address


def get_all(user_id: int, db: Session):
    if db_check_methods.check_admin_status(user_id, db):
        return db.query(DbAddress).all()
    else:
        return db.query(DbAddress).filter(
            DbAddress.user_id == user_id).all()


def get_single_by_id(id: int, user_id: int, db: Session):
    targeted_address = db_check_methods.check_address_id(id, db).first()
    if db_check_methods.check_admin_status(user_id, db) or user_id == targeted_address.user_id:
        return targeted_address


def update(user_id: int, address_id: int, request: address_schemas.AddressBase, db: Session):
    targeted_address = db_check_methods.check_address_id(address_id, db)
    db_check_methods.admin_only_method(user_id, db)
    if targeted_address.first().user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="This method is not allowed."
        )
    targeted_address.update(request.dict())
    db.commit()
    return targeted_address.first()


def change_user_id(address_id: int, new_user_id: int, user_id: int, db: Session):
    targeted_address = db_check_methods.check_address_id(address_id, db)
    if db_check_methods.check_admin_status(user_id, db):
        db_check_methods.check_user_id(new_user_id, db)
        data_to_update = dict(user_id=new_user_id)
        targeted_address.update(data_to_update)
        db.commit()
        return targeted_address.first()


def deactivate_address(address_id: int, user_id: int, db: Session):
    targeted_address = db_check_methods.check_address_id(address_id, db)
    if not db_check_methods.check_admin_status(user_id, db) and targeted_address.first().user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="Method is not allowed."
        )
    data_to_update = dict(active_address=False)
    targeted_address.update(data_to_update)
    db.commit()
    return targeted_address.first()


def activate_address(address_id: int, user_id: int, db: Session):
    targeted_address = db_check_methods.check_address_id(address_id, db)
    if not db_check_methods.check_admin_status(user_id, db) and targeted_address.first().user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="Method is not allowed."
        )
    data_to_update = dict(active_address=False)
    targeted_address.update(data_to_update)
    db.commit()
    return targeted_address.first()

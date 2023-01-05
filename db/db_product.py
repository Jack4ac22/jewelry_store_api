from sqlalchemy.orm.session import Session
from schemas import product_schemas
from .models import DbProduct
from db import db_check_methods
from fastapi import HTTPException, status


def create_product(request: product_schemas.ProductBase, user_id: int, db: Session):
    if not db_check_methods.check_admin_status(user_id, db):
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="The method is reserved for admins."
        )
    new_product = DbProduct(added_by=user_id, **request.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


def get_all(db: Session):
    return db.query(DbProduct).all()


def get_one(id: int, db: Session):
    return db_check_methods.check_product_id(id, db).first()


def update_product(id: int, request: product_schemas.ProductBase, user_id: int, db: Session):
    db_check_methods.admin_only_method(user_id, db)
    targeted_product = db_check_methods.check_product_id(id, db)
    targeted_product.update(request.dict())
    db.commit()
    return targeted_product.first()


def reverse_featured(id: int, user_id: int, db: Session):
    db_check_methods.admin_only_method(user_id, db)
    targeted_product = db_check_methods.check_product_id(id, db)
    new_status = not targeted_product.first().featured
    targeted_product.update({"featured": new_status})
    db.commit()
    return targeted_product.first()


def reverse_hidden(id: int, user_id: int, db: Session):
    db_check_methods.admin_only_method(user_id, db)
    targeted_product = db_check_methods.check_product_id(id, db)
    new_status = not targeted_product.first().hidden
    targeted_product.update({"hidden": new_status})
    db.commit()
    return targeted_product.first()


def delete(id: int, user_id: int, db: Session):
    db_check_methods.admin_only_method(user_id, db)
    targeted_product = db_check_methods.check_product_id(id, db)
    deleted_data = targeted_product.first()
    targeted_product.delete()
    db.commit()
    return deleted_data

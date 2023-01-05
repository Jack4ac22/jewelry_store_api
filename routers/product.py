from db import db_check_methods, db_product
from db.database import get_db
from fastapi import APIRouter, Depends, status
from schemas import product_schemas
from sqlalchemy.orm.session import Session
from typing import List, Union
from utilities import jwt_manager

router = APIRouter(
    prefix="/product",
    tags=["product"]
)


@router.post('', status_code=status.HTTP_201_CREATED, response_model=product_schemas.ProductDisplay)
def create_new_product(request: product_schemas.ProductBase, user_id: int = Depends(jwt_manager.decode_token_id), db: Session = Depends(get_db)):
    return db_product.create_product(request, user_id, db)


@router.get("/all", response_model=Union[List[product_schemas.ProductDisplaySimple], None])
def get_all_products(db: Session = Depends(get_db)):
    return db_product.get_all(db)


@router.get("/{product_id}", response_model=product_schemas.ProductDisplaySimple)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    return db_product.get_one(product_id, db)


@router.put("/featured{product_id}",
            response_model=product_schemas.ProductDisplay)
def reverse_product_featured_status(product_id: int, user_id: int = Depends(jwt_manager.decode_token_id), db: Session = Depends(get_db)):
    return db_product.reverse_featured(product_id, user_id, db)


@router.put("/hidden{product_id}",
            response_model=product_schemas.ProductDisplay)
def reverse_product_hidden_status(product_id: int, user_id: int = Depends(jwt_manager.decode_token_id), db: Session = Depends(get_db)):
    return db_product.reverse_hidden(product_id, user_id, db)


@router.put("/{product_id}", response_model=product_schemas.ProductDisplay)
def update_product_by_id(product_id: int, request: product_schemas.ProductBase, user_id: int = Depends(jwt_manager.decode_token_id), db: Session = Depends(get_db)):
    return db_product.update_product(product_id, request, user_id, db)


@router.delete("/{product_id}", response_model=product_schemas.ProductDisplaySimple)
def delete_product_by_id(product_id: int, user_id: int = Depends(jwt_manager.decode_token_id), db: Session = Depends(get_db)):
    return db_product.delete(product_id, user_id, db)

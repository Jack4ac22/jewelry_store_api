from sqlalchemy.orm.session import Session
from fastapi import APIRouter, Depends, status
from db.database import get_db
from schemas import address_schemas, user_schemas, other_schemas
from db import db_address, db_check_methods
from typing import Union, List
from utilities import jwt_manager

router = APIRouter(
    prefix="/address",
    tags=["address"]
)


@router.post("/{address_user_id}", response_model=address_schemas.AddressDisplay, status_code=status.HTTP_201_CREATED, description="Admins will be able to add addresses to any user, the id of the non-Admin users will automatically be used in the creation of the address.")
def create_new_address(address_user_id: int, request: address_schemas.AddressBase, user_id: int = Depends(jwt_manager.decode_token_id), db: Session = Depends(get_db)):
    return db_address.create_address(address_user_id, user_id, request, db)


@router.get("/all", response_model=List[address_schemas.AddressDisplay])
def get_all_addresses(user_id: int = Depends(jwt_manager.decode_token_id), db: Session = Depends(get_db)):
    return db_address.get_all(user_id, db)


@router.get("/{address_id}", response_model=Union[address_schemas.AddressDisplay, None], response_description="Only admins and the address owner will be able to retrieve the targeted address, otherwise, the response will be null.")
def get_address_by_id(address_id: int, user_id: int = Depends(jwt_manager.decode_token_id), db: Session = Depends(get_db)):
    return db_address.get_single_by_id(address_id, user_id, db)


@router.put("/update/{address_id}", response_model=address_schemas.AddressDisplay)
def update_address(
        address_id: int,
        request: address_schemas.AddressBase,
        user_id: int = Depends(jwt_manager.decode_token_id),
        db: Session = Depends(get_db)):
    return db_address.update(user_id, address_id, request, db)


@router.put("/update/{address_id}/{new_user_id}", response_model=address_schemas.AddressDisplay)
def change_user_of_address(address_id: int, new_user_id: int, user_id: int = Depends(jwt_manager.decode_token_id), db: Session = Depends(get_db)):
    return db_address.change_user_id(address_id, new_user_id, user_id, db)


@router.put("/deactivate/{address_id}", response_model=address_schemas.AddressDisplay)
def deactivate_address_by_id(address_id: int, user_id: int = Depends(jwt_manager.decode_token_id), db: Session = Depends(get_db)):
    return db_address.deactivate_address(address_id, user_id, db)


@router.put("/activate/{address_id}", response_model=address_schemas.AddressDisplay)
def activate_address_by_id(address_id: int, user_id: int = Depends(jwt_manager.decode_token_id), db: Session = Depends(get_db)):
    return db_address.activate_address(address_id, user_id, db)

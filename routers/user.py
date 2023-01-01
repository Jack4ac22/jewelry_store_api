from fastapi import APIRouter, Depends
from db.database import get_db
from schemas import user_schemas
from sqlalchemy.orm.session import Session
from db.db_user import create_user
router = APIRouter(
    prefix='/user',
    tags=['user']
)


@router.post('', response_model=user_schemas.UserDisplay, response_description="the created user will be returned without the password.")
def create_new_user(request: user_schemas.UserBase, db: Session = Depends(get_db)):
    return create_user(request, db)

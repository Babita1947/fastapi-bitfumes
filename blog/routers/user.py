from fastapi import APIRouter, Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from .. import schemas, database
from ..repository import user


router = APIRouter(
    prefix="/user",
    tags=["Users"]
)


pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post('/', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(database.get_db)):
    return user.create(request, db)

@router.get('/{id}', response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(database.get_db)):
    return user.get(id, db)
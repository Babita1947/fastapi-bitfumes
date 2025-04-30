from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from .. import models, schemas, database, hashing



router = APIRouter()


pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post('/user', response_model=schemas.ShowUser, tags=["users"])
def create_user(request: schemas.User, db: Session = Depends(database.get_db)):

    new_user = models.User(name = request.name, email = request.email, password = hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/user/{id}', response_model=schemas.ShowUser, tags=["users"])
def get_user(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} is not available")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'details': f"Blog with the id {id} is not available"}
    return user
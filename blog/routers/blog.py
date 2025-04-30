from typing import List
from fastapi import APIRouter, Depends, status, HTTPException, Response

from .. import models, schemas, database
from sqlalchemy.orm import Session


router = APIRouter()

@router.get("/blog", tags=["blogs"], response_model=List[schemas.ShowBlog])
def all(db:Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@router.post('/blog', status_code=status.HTTP_201_CREATED, tags=["blogs"])
def create(request: schemas.Blog, db: Session = Depends(database.get_db)):
    new_blog = models.Blog(title = request.title, body = request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["blogs"])
def destroy(id, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog id {id} not found")
    db.delete(blog)
    db.commit()
    return 'done'


@router.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=["blogs"])
def update(id, request: schemas.Blog, db: Session = Depends(database.get_db)):
    print("-----------------------------------",request)
    data = {
        "title":request.title,
        "body":request.body
    }
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=404, detail=f"Blog id {id} not found")
    blog.update(data)
    db.commit()
    return {"message": "Updated successfully"}


@router.get('/blog/{id}', status_code=status.HTTP_200_OK, tags=["blogs"])
def show(id, response: Response, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'details': f"Blog with the id {id} is not available"}
    return blog

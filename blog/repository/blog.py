from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas

def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs

def create(request: schemas.Blog,db: Session):
    new_blog = models.Blog(title = request.title, body = request.body, user_id = request.user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def delete(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog id {id} not found")
    db.delete(blog)
    db.commit()
    return {"message": "Deleted Successfully"}

def update(id: int, request: schemas.Blog, db: Session):
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
    return {"message": "Updated Successfully"}

def show(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'details': f"Blog with the id {id} is not available"}
    return blog
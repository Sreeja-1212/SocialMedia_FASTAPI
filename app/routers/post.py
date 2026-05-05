from typing import Optional
from unittest import skip
from sqlalchemy import func
from app import models, utils
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils import hash_password
import app.Schema as schemas
import app.oauth2 as oauth2
from typing import Optional


router = APIRouter(
    prefix = "/posts",
    tags = ["Posts"]
)




@router.get("/", response_model=list[schemas.PostOut])
async def get_posts(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user), limit: int = 10,skip: int = 0, search: Optional[str] = ""):
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # using SQLAlchemy ORM to query all posts from the database - returns a list of Post objects
    return results # return the list of posts as the response to the API request - FastAPI will automatically convert the list of Post objects to JSON format based on the response_model defined in the route decorator


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def create_posts(post:schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    
    new_post = models.Post(**post.model_dump(), owner_id=current_user.id) # create a new Post object using the data from the request body
    db.add(new_post) 
    db.commit() 
    # refresh the new_post object to get the generated id and other fields from the database - ensures that the new_post object has all the updated data after being added to the database
    db.refresh(new_post) 
    return new_post



@router.get("/{id}",response_model=schemas.PostOut) # here id is path parameter
async def get_post(id: int, db: Session = Depends(get_db),current_user: models.User = Depends(oauth2.get_current_user)): # path parameters are always strings need to convert to int
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    print(post)
    if post:
        return post
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    stored_post = post_query.first()
    if not stored_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    if stored_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
async def update_post(id:int, post:schemas.PostUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return updated_post

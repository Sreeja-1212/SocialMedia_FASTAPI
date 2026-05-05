from app import models, utils
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils import hash_password
import app.Schema as schemas
from app import oauth2


router = APIRouter(
    tags = ["Authentication"]
)

@router.post("/login",response_model=schemas.Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid email or password")
    
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid email or password")
    
    #create a JWT token and return it, data is the payload to the token
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    print(access_token)
    return {"access_token": access_token, "token_type": "bearer"}



    
   
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    password: str

class UserCreate(UserBase):
    pass

class UserResponse(BaseModel):
    email: EmailStr
    created_at: datetime
    id: int
    model_config = ConfigDict(from_attributes=True)  

class UserLogin(UserBase):
    pass

class Postbase(BaseModel):
    title : str
    content: str
    published: bool = True

class PostCreate(Postbase):
    pass

class PostUpdate(Postbase):
    pass


class PostResponse(Postbase):
    id: int
    created_at: datetime
    owner_id :int
    owner: UserResponse
    model_config = ConfigDict(from_attributes=True) # tells Pydantic to read data from the attributes of the SQLAlchemy model instance - allows us to return SQLAlchemy model instances directly from our path operations and have them automatically converted to the appropriate response models based on the defined fields and their types

class PostOut(BaseModel):
    Post: PostResponse
    votes: int

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: int | None = None

class Vote(BaseModel):
    post_id: int
    dir: int

    
    
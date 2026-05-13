
from fastapi import FastAPI
from app.database import engine
from app.database import Base
from app.routers import auth, post, users, vote
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware



origins = [
   "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"message": "Hello World"}
# call instance of FASTAPI class
app = FastAPI()

# Create tables in the database
# Base.metadata.create_all(bind=engine)
# commented out because we will use Alembic for database migrations instead of creating tables directly from the models - allows us to manage changes to the database schema over time in a more controlled and organized way, with the ability to apply and rollback changes as needed


# include the routers for posts and users - organizes the API endpoints into separate modules for better maintainability and scalability
app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)



@app.get("/")
async def root():
    return {"message": "Welcome to my API"}











   

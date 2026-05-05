# deals with database connection and session management
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app import config

# SQLALCHEMY_DATABASE_URL is the connection string for the database
# format: "postgresql+psycopg2://user:password@host:port/database_name"
SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{config.settings.database_username}:{config.settings.database_password}@{config.settings.database_hostname}:{config.settings.database_port}/{config.settings.database_name}"


# engine manages connections to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Sessions manages transactions with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base manages meta data for tables
Base = declarative_base()

# Dependency to get DB session
# will be used in path operations to interact with the database - ensures that a new session is created for each request and properly closed after the request is finished
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



from config import setting
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import Generator


SQLALCHEMY_DATABASE_URL = setting.DATABASE_URL


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)
##SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
##autocomit ra autoflush kaam na huda samma paraena bolauna
Base = declarative_base()

#dependency injection
def get_db() -> Generator:
    try:
        db = SessionLocal()
        ## created db object
        yield db
        ## return db
    finally:
        db.close()

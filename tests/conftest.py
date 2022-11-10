from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


import pytest
import os
import sys


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
##we imported os and sys and gave above command to get the path of main
##do it before calling main to let know where it resides

from main import app
from database import Base, get_db
from config import setting
from models import User
from hashing import Hasher


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)   ##sqlite ma db banako // not to use production db


TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base.metadata.create_all(bind=engine)


@pytest.fixture
    #this forces fixture to be called first
    ##and then only the remaining test cases
def client():
    def override_get_db():
        try:
            db = TestingSessionLocal()
            ## created db object
            yield db
            ## return db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
        #we are using yield instead of return


@pytest.fixture
    #this forces fixture to be called first
    ##and then only the remaining test cases
def token_header(client: TestClient):
    #as our client is Testclient
    #we need to use db
    test_email = setting.TEST_EMAIL
    test_pass = setting.TEST_PASS
    #test tala halda error aayo so mail and pass yeta halya
    #ani tala call garaeko teslai
    db = TestingSessionLocal()
    user = db.query(User).filter(User.email==test_email).first()
    if user is None:
        user = User(email=test_email, password=Hasher.get_hash_password(test_pass))
        db.add(user)
        db.commit()
        db.refresh(user)

    data = {"username":test_email, "password":test_pass}
        #username and password any user we have in our test.db
        #since they are as dictionary we use above syntax
    response = client.post("/login/token", data=data)
    access_token = response.json()["access_token"]
        #as the response is json, thei anusar data fetch garaeko
        #also we have defines access_token in login.py
            #check that for reference if needed
    return {"Authorization": f"Bearer {access_token}"}

from pydantic import EmailStr, BaseModel
from datetime import date


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class ShowUser(BaseModel):
    email: EmailStr
    is_active: bool

    class Config:
        orm_mode=True
        ##orm object relationship mapper
        ##object lai dictionary banayo


class ItemCreate(BaseModel):
    title: str
    description: str


class ShowItem(BaseModel):
    title: str
    description: str
    date_posted: date

    class Config:
        orm_mode=True

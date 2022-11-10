from fastapi import FastAPI
from config import setting
from database import engine
from models import Base
from routers import users, items, login

Base.metadata.create_all(bind=engine)

description = '''
### This is my app
Route is *INDEX*
'''

tags = [
    {
        "name": "user",
        "description": "user routes"
    },
    {
        "name": "items",
        "description": "order related route"
    }
]
##tags= [..{},..] diff tags banaucha

app = FastAPI(
    title=setting.TITLE,
    description=setting.DESCRIPTION,
    version=setting.VERSION,
    contact={
        "name": setting.NAME,
        "email": setting.EMAIL
    }
)


app.include_router(users.router)
app.include_router(items.router)
app.include_router(login.router)

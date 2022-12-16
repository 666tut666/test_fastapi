from fastapi import FastAPI
from config import setting
from database import engine
from models import Base
from routers import users, items, login
from webapps.routers import items as web_items, users as web_users, auth as web_auth
from fastapi.staticfiles import StaticFiles

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
##tags= [{...}, {...}] diff tags banaucha

app = FastAPI(
    title=setting.TITLE,
    description=setting.DESCRIPTION,
    version=setting.VERSION,
    contact={
        "name": setting.NAME,
        "email": setting.EMAIL
    }
)


app.mount("/static", StaticFiles(directory="static"), name="static")
    #mount the path for img


app.include_router(users.router)
app.include_router(items.router)
app.include_router(login.router)
app.include_router(web_items.router)
app.include_router(web_users.router)
app.include_router(web_auth.router)

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from models import Items, User
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="templates")
    #defined path where html files are
        ##templates.....


@router.get("/")
def item_home(
        request: Request,
        db:Session=Depends(get_db),
        msg:str=None
):
    items = db.query(Items).all()
    return templates.TemplateResponse("item_hp.html", {"request": request, "items": items, "msg": msg})
        #using pydantic approach
        ##taking i/p: as request// request type
            #item_hp.html is item`s home page
            ##gotta declare Request in Jinja
        ## as we have used item_hp, gotta define it there too


@router.get("/detail/{id}")
def item_detail(
        request: Request,
        id: int,
        db: Session = Depends(get_db)
):
    item = db.query(Items).filter(Items.id==id).first()
    user = db.query(User).filter(User.id==item.owner_id).first()
    return templates.TemplateResponse(
        "item_detail.html",
        {
            "request": request,
            "item": item,
            "user": user
        }
    )


@router.get("/create-an-item")
def create_an_item(request: Request):
    return templates.TemplateResponse(
        "create_item.html",
        {"request": request}
    )

#using post method for submit button
@router

from fastapi import APIRouter, Depends, HTTPException, status
from schemas import ItemCreate, ShowItem
from models import Items, User
from datetime import datetime
from sqlalchemy.orm import Session
from database import get_db
from typing import List
from fastapi.encoders import jsonable_encoder
from routers.login import oath2_scheme
from jose import jwt
from config import setting

router = APIRouter()


def get_user_from_token(db, token):
    ##using try block
    try:
        payload = jwt.decode(token, setting.SECRET_KEY, algorithms=setting.ALGORITHM)
        username = payload.get("sub")
        # data is dictionary,
        # payload.get is a dictionary method to get data.
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unable to verify"
            )
        user = db.query(User).filter(User.email == username).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="email is not in our database"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unable to verify"
        )
    return user


@router.post(
    "/item",
    tags=["items"],
    response_model=ShowItem
)
def create_item(
        item: ItemCreate,
        db: Session = Depends(get_db),
        token:str=Depends(oath2_scheme)
):
    # token:... to accept the token
    user = get_user_from_token(db, token)
    owner_id = user.id
    date_posted = datetime.now().date()
    item = Items(
        **item.dict(),
        date_posted=date_posted,
        owner_id=owner_id
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/item/all", tags=["items"], response_model=List[ShowItem])
    #show item matra rakhda error aayo,
    #so, added List
def retrieve_all_items(db: Session=Depends(get_db)):
    items = db.query(Items).all()
    return items


@router.get("/item/{id}", tags=["items"])
def retrieve_item_by_id(id, db: Session = Depends(get_db)):
        #get_db as we need to retrieve id from the database
    item = db.query(Items).filter(Items.id==id).first()
        #filter to filter whatever
        #.first to return first item
    if not item:    ##if item is null
        raise HTTPException(status_code=404, detail=f"Item {id} does not exist")
    return item


#using jsonable encoder
@router.put("/item/update/{id}", tags=["items"])
def update_item_by_id(
        id:int,
        item:ItemCreate,
        db:Session=Depends(get_db),
        token:str=Depends(oath2_scheme)
):
    user = get_user_from_token(db, token)
    existing_item = db.query(Items).filter(Items.id==id)
        #it only returns query
    if not existing_item.first():
            #.first() to fetch details
        return {"Message": f"Item ID {id} has no details "}
    if existing_item.first().owner_id == user.id:
        existing_item.update(jsonable_encoder(item))
        db.commit()
        return {"message": f"details for {id} Successfully Updated"}
    else:
        return {"message": "you aren`t authorized"}

#using __dict__
@router.put("/item/update1/{id}", tags=["items"])
def update_item_by_id_using_dict(
        id:int,
        item:ItemCreate,
        db:Session=Depends(get_db),
        token:str=Depends(oath2_scheme)
):
    existing_item = db.query(Items).filter(Items.id==id)
        #it only returns query
    if not existing_item.first():
            #.first() to fetch details
        return {"Message": f"Item ID {id} has no details "}
    existing_item.update(item.__dict__)
    db.commit()
    return {"message": f"details for {id} Successfully Updated"}


@router.delete("/item/delete/{id}", tags=["items"])
def delete_item_by_id(
        id:int,
        db:Session=Depends(get_db),
        token:str=Depends(oath2_scheme)
):
    user = get_user_from_token(db, token)
    existing_item = db.query(Items).filter(Items.id == id)
        # it only returns query
    if not existing_item.first():
            #.first() to fetch details
        return {"Message": f"Item ID {id} has no details "}
    if existing_item.first().owner_id == user.id:
        existing_item.delete()
        db.commit()
        return {"message": f"Item id: {id} Successfully Deleted"}
    else:
        return {"message": "you aren`t authorized"}

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, database
from app.crud import menus, restaurants

router = APIRouter()


@router.post("/{restaurant_id}/menu/", response_model=schemas.MenuItem)
def create_menu_item(restaurant_id: int, menu_item: schemas.MenuItemCreate, db: Session = Depends(database.get_db)):
    db_restaurant = restaurants.get_restaurant(db, restaurant_id=restaurant_id)
    if db_restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return menus.create_menu_item(db=db, menu_item=menu_item, restaurant_id=restaurant_id)


@router.get("/{restaurant_id}/menu/", response_model=list[schemas.MenuItem])
def get_menu_items(restaurant_id: int, db: Session = Depends(database.get_db)):
    return menus.get_menu_items(db, restaurant_id=restaurant_id)

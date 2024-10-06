from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import database
from app.schemas import menus as menus_s
from app.crud import menus, restaurants

router = APIRouter()


@router.post("/{restaurant_id}/menu/", response_model=menus_s.MenuItem)
def create_menu_item(restaurant_id: int, menu_item: menus_s.MenuItemCreate, db: Session = Depends(database.get_db)):
    db_restaurant = restaurants.get_restaurant(db, restaurant_id=restaurant_id)
    if db_restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return menus.create_menu_item(db=db, menu_item=menu_item, restaurant_id=restaurant_id)


@router.get("/{restaurant_id}/menu/", response_model=list[menus_s.MenuItem])
def get_menu_items(restaurant_id: int, db: Session = Depends(database.get_db)):
    return menus.get_menu_items(db, restaurant_id=restaurant_id)


@router.put("/menu/{menu_item_id}", response_model=menus_s.MenuItem)
def update_menu_item(menu_item_id: int, menu_item: menus_s.MenuItemCreate, db: Session = Depends(database.get_db)):
    db_menu_item = menus.update_menu_item(db, menu_item_id=menu_item_id, menu_item=menu_item)
    if db_menu_item is None:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return db_menu_item


@router.delete("/menu/{menu_item_id}", response_model=menus_s.MenuItem)
def delete_menu_item(menu_item_id: int, db: Session = Depends(database.get_db)):
    db_menu_item = menus.delete_menu_item(db, menu_item_id=menu_item_id)
    if db_menu_item is None:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return db_menu_item

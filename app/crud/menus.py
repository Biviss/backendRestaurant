from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app import models, schemas


def create_menu_item(db: Session, menu_item: schemas.MenuItemCreate, restaurant_id: int) -> schemas.MenuItem:
    db_menu_item = models.MenuItem(**menu_item.dict(), restaurant_id=restaurant_id)
    db.add(db_menu_item)

    try:
        db.commit()
        db.refresh(db_menu_item)
    except IntegrityError:
        db.rollback()
        raise ValueError("This menu already exists.")

    return schemas.MenuItem.from_orm(db_menu_item)


def get_menu_items(db: Session, restaurant_id: int) -> list[schemas.MenuItem]:
    menu_items = db.query(models.MenuItem).filter(models.MenuItem.restaurant_id == restaurant_id).all()
    return [schemas.MenuItem.from_orm(item) for item in menu_items]

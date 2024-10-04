from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app import models, schemas


def get_restaurants(db: Session, skip: int = 0, limit: int = 10) -> list[schemas.Restaurant]:
    restaurants = db.query(models.Restaurant).offset(skip).limit(limit).all()
    return [schemas.Restaurant.from_orm(restaurant) for restaurant in restaurants]


def create_restaurant(db: Session, restaurant: schemas.RestaurantCreate) -> schemas.Restaurant:
    db_restaurant = models.Restaurant(**restaurant.dict())
    db.add(db_restaurant)

    try:
        db.commit()
        db.refresh(db_restaurant)
    except IntegrityError:
        db.rollback()
        raise ValueError("This restaurant is exist.")

    return schemas.Restaurant.from_orm(db_restaurant)


def create_menu_item(db: Session, menu_item: schemas.MenuItemCreate, restaurant_id: int) -> schemas.MenuItem:
    db_menu_item = models.MenuItem(**menu_item.dict(), restaurant_id=restaurant_id)
    db.add(db_menu_item)

    try:
        db.commit()
        db.refresh(db_menu_item)
    except IntegrityError:
        db.rollback()
        raise ValueError("This menu in exist.")

    return schemas.MenuItem.from_orm(db_menu_item)


def get_menu_items(db: Session, restaurant_id: int) -> list[schemas.MenuItem]:
    menu_items = db.query(models.MenuItem).filter(models.MenuItem.restaurant_id == restaurant_id).all()
    return [schemas.MenuItem.from_orm(item) for item in menu_items]


def get_restaurant(db: Session, restaurant_id: int):
    return db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()


def update_restaurant(db: Session, restaurant_id: int,
                      restaurant: schemas.RestaurantCreate) -> models.Restaurant | None:
    db_restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()

    if db_restaurant is None:
        return None

    for key, value in restaurant.dict().items():
        setattr(db_restaurant, key, value)

    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant


def delete_restaurant(db: Session, restaurant_id: int) -> models.Restaurant | None:
    db_restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()

    if db_restaurant is None:
        return None

    db.delete(db_restaurant)
    db.commit()
    return db_restaurant

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.schemas import restaurants
from app.models import models


def get_restaurants(db: Session, skip: int = 0, limit: int = 10) -> list[restaurants.Restaurant]:
    restaurants_in = db.query(models.Restaurant).offset(skip).limit(limit).all()
    return [restaurants.Restaurant.from_orm(restaurant) for restaurant in restaurants_in]


def create_restaurant(db: Session, restaurant: restaurants.RestaurantCreate) -> restaurants.Restaurant:
    db_restaurant = models.Restaurant(**restaurant.dict())
    db.add(db_restaurant)

    try:
        db.commit()
        db.refresh(db_restaurant)
    except IntegrityError:
        db.rollback()
        raise ValueError("This restaurant already exists.")

    return restaurants.Restaurant.from_orm(db_restaurant)


def get_restaurant(db: Session, restaurant_id: int):
    return db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()


def update_restaurant(db: Session, restaurant_id: int, restaurant: restaurants.RestaurantCreate) -> models.Restaurant | None:
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

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.schemas import restaurants
from app.models import models


def get_restaurants(db: Session, skip: int = 0, limit: int = 10) -> list[restaurants.Restaurant]:
    """
        Retrieves a list of restaurants.

        Args:
            db (Session): The database session.
            skip (int, optional): Number of records to skip. Defaults to 0.
            limit (int, optional): Maximum number of records to return. Defaults to 10.

        Returns:
            list[restaurants.Restaurant]: A list of restaurants within the specified range.
        """
    restaurants_in = db.query(models.Restaurant).offset(skip).limit(limit).all()
    return [restaurants.Restaurant.from_orm(restaurant) for restaurant in restaurants_in]


def create_restaurant(db: Session, restaurant: restaurants.RestaurantCreate) -> restaurants.Restaurant:
    """
        Creates a new restaurant.

        Args:
            db (Session): The database session.
            restaurant (restaurants.RestaurantCreate): Data for creating a new restaurant.

        Returns:
            restaurants.Restaurant: The new created restaurant.

        Raises:
            ValueError: If the restaurant already exists in the database.
        """
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
    """
        Get a restaurant.

        Args:
            db (Session): The database session.
            restaurant_id (int): The ID of the restaurant.

        Returns:
            models.Restaurant | None: The restaurant with the specified ID, or None if not found.
        """
    return db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()


def update_restaurant(db: Session, restaurant_id: int, restaurant: restaurants.RestaurantCreate) -> models.Restaurant | None:
    """
            Updates the restaurant.

            Args:
                db (Session): The database session.
                restaurant_id (int): The ID of the restaurant.
                restaurant (restaurants.RestaurantCreate): The updated restaurant data.

            Returns:
                models.Restaurant | None: The updated restaurant object, or None if the restaurant was not found.
            """
    db_restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()

    if db_restaurant is None:
        return None

    for key, value in restaurant.dict().items():
        setattr(db_restaurant, key, value)

    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant


def delete_restaurant(db: Session, restaurant_id: int) -> models.Restaurant | None:
    """
            Deletes a restaurant.

            Args:
                db (Session): The database session.
                restaurant_id (int): The ID of the restaurant.

            Returns:
                models.Restaurant | None: The deleted restaurant object, or None if the restaurant was not found.
            """
    db_restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()

    if db_restaurant is None:
        return None

    db.delete(db_restaurant)
    db.commit()
    return db_restaurant

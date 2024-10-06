from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import database
from app.schemas import restaurants as restaurants_s
from app.crud import restaurants

router = APIRouter()


@router.get("/", response_model=list[restaurants_s.Restaurant])
def read_restaurants(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    get_restaurants = restaurants.get_restaurants(db, skip=skip, limit=limit)
    return get_restaurants


@router.post("/", response_model=restaurants_s.Restaurant)
def create_restaurant(restaurant: restaurants_s.RestaurantCreate, db: Session = Depends(database.get_db)):
    return restaurants.create_restaurant(db=db, restaurant=restaurant)


@router.put("/{restaurant_id}", response_model=restaurants_s.Restaurant)
def update_restaurant(
        restaurant_id: int,
        restaurant: restaurants_s.RestaurantCreate,
        db: Session = Depends(database.get_db)
):
    db_restaurant = restaurants.get_restaurant(db, restaurant_id=restaurant_id)
    if db_restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    return restaurants.update_restaurant(db=db, restaurant_id=restaurant_id, restaurant=restaurant)


@router.delete("/{restaurant_id}", response_model=restaurants_s.Restaurant)
def delete_restaurant(restaurant_id: int, db: Session = Depends(database.get_db)):
    db_restaurant = restaurants.get_restaurant(db, restaurant_id=restaurant_id)
    if db_restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurants.delete_restaurant(db=db, restaurant_id=restaurant_id)

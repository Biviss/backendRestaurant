from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database

router = APIRouter()


@router.get("/", response_model=list[schemas.Restaurant])
def read_restaurants(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    restaurants = crud.get_restaurants(db, skip=skip, limit=limit)
    return restaurants


@router.post("/", response_model=schemas.Restaurant)
def create_restaurant(restaurant: schemas.RestaurantCreate, db: Session = Depends(database.get_db)):
    return crud.create_restaurant(db=db, restaurant=restaurant)


@router.put("/{restaurant_id}", response_model=schemas.Restaurant)
def update_restaurant(
        restaurant_id: int,
        restaurant: schemas.RestaurantCreate,
        db: Session = Depends(database.get_db)
):
    db_restaurant = crud.get_restaurant(db, restaurant_id=restaurant_id)
    if db_restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    return crud.update_restaurant(db=db, restaurant_id=restaurant_id, restaurant=restaurant)


@router.delete("/{restaurant_id}", response_model=schemas.Restaurant)
def delete_restaurant(restaurant_id: int, db: Session = Depends(database.get_db)):
    db_restaurant = crud.get_restaurant(db, restaurant_id=restaurant_id)
    if db_restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return crud.delete_restaurant(db=db, restaurant_id=restaurant_id)

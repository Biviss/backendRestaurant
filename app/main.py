from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, crud, database, schemas
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, get_db


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=database.engine)


@app.get("/")
def home():
    return {"data": "Restourant API"}


@app.get("/restaurants/", response_model=list[schemas.Restaurant])
def read_restaurants(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    restaurants = crud.get_restaurants(db, skip=skip, limit=limit)
    return restaurants


@app.post("/restaurants/", response_model=schemas.Restaurant)
def create_restaurant(restaurant: schemas.RestaurantCreate, db: Session = Depends(database.get_db)):
    return crud.create_restaurant(db=db, restaurant=restaurant)


@app.post("/restaurants/{restaurant_id}/menu/", response_model=schemas.MenuItem)
def create_menu_item(restaurant_id: int, menu_item: schemas.MenuItemCreate, db: Session = Depends(get_db)):
    db_restaurant = crud.get_restaurant(db, restaurant_id=restaurant_id)
    if db_restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return crud.create_menu_item(db=db, menu_item=menu_item, restaurant_id=restaurant_id)


@app.get("/restaurants/{restaurant_id}/menu/", response_model=list[schemas.MenuItem])
def get_menu_items(restaurant_id: int, db: Session = Depends(get_db)):
    return crud.get_menu_items(db, restaurant_id=restaurant_id)


@app.put("/restaurants/{restaurant_id}", response_model=schemas.Restaurant)
def update_restaurant(
        restaurant_id: int,
        restaurant: schemas.RestaurantCreate,
        db: Session = Depends(get_db)
):
    db_restaurant = crud.get_restaurant(db, restaurant_id=restaurant_id)
    if db_restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    return crud.update_restaurant(db=db, restaurant_id=restaurant_id, restaurant=restaurant)


@app.delete("/restaurants/{restaurant_id}", response_model=schemas.Restaurant)
def delete_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    db_restaurant = crud.get_restaurant(db, restaurant_id=restaurant_id)
    if db_restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return crud.delete_restaurant(db=db, restaurant_id=restaurant_id)

from fastapi import FastAPI
from app import models
from app.database import engine
from fastapi.middleware.cors import CORSMiddleware
from app.routers import restaurants, menus


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"data": "Restourant API"}


app.include_router(restaurants.router, prefix="/restaurants", tags=["Restaurants"])
app.include_router(menus.router, prefix="/restaurants", tags=["Menu"])


# @app.get("/restaurants/", response_model=list[schemas.Restaurant])
# def read_restaurants(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
#     restaurants = crud.get_restaurants(db, skip=skip, limit=limit)
#     return restaurants
#
#
# @app.post("/restaurants/", response_model=schemas.Restaurant)
# def create_restaurant(restaurant: schemas.RestaurantCreate, db: Session = Depends(database.get_db)):
#     return crud.create_restaurant(db=db, restaurant=restaurant)
#
#
# @app.post("/restaurants/{restaurant_id}/menu/", response_model=schemas.MenuItem)
# def create_menu_item(restaurant_id: int, menu_item: schemas.MenuItemCreate, db: Session = Depends(get_db)):
#     db_restaurant = crud.get_restaurant(db, restaurant_id=restaurant_id)
#     if db_restaurant is None:
#         raise HTTPException(status_code=404, detail="Restaurant not found")
#     return crud.create_menu_item(db=db, menu_item=menu_item, restaurant_id=restaurant_id)
#
#
# @app.get("/restaurants/{restaurant_id}/menu/", response_model=list[schemas.MenuItem])
# def get_menu_items(restaurant_id: int, db: Session = Depends(get_db)):
#     return crud.get_menu_items(db, restaurant_id=restaurant_id)
#
#
# @app.put("/restaurants/{restaurant_id}", response_model=schemas.Restaurant)
# def update_restaurant(
#         restaurant_id: int,
#         restaurant: schemas.RestaurantCreate,
#         db: Session = Depends(get_db)
# ):
#     db_restaurant = crud.get_restaurant(db, restaurant_id=restaurant_id)
#     if db_restaurant is None:
#         raise HTTPException(status_code=404, detail="Restaurant not found")
#
#     return crud.update_restaurant(db=db, restaurant_id=restaurant_id, restaurant=restaurant)
#
#
# @app.delete("/restaurants/{restaurant_id}", response_model=schemas.Restaurant)
# def delete_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
#     db_restaurant = crud.get_restaurant(db, restaurant_id=restaurant_id)
#     if db_restaurant is None:
#         raise HTTPException(status_code=404, detail="Restaurant not found")
#     return crud.delete_restaurant(db=db, restaurant_id=restaurant_id)

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

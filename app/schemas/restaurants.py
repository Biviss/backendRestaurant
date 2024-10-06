from pydantic import BaseModel


class RestaurantBase(BaseModel):
    name: str
    contact: str
    address: str
    open_hours: str

    class Config:
        orm_mode = True
        from_attributes = True


class Restaurant(RestaurantBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True


class RestaurantCreate(RestaurantBase):
    pass

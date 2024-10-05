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


class MenuItemBase(BaseModel):
    name: str
    day: str
    price: float

    class Config:
        orm_mode = True
        from_attributes = True


class MenuItem(MenuItemBase):
    id: int
    restaurant_id: int

    class Config:
        orm_mode = True
        from_attributes = True


class MenuItemCreate(MenuItemBase):
    pass

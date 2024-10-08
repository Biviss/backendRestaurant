from pydantic import BaseModel


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

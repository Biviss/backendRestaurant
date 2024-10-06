from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.schemas import menus
from app.models import models


def create_menu_item(db: Session, menu_item: menus.MenuItemCreate, restaurant_id: int) -> menus.MenuItem:
    """
        Creates a new menu item for the restaurant.

        Args:
            db (Session): The database session.
            menu_item (menus.MenuItemCreate): Data for creating a new menu item.
            restaurant_id (int): The ID of the restaurant.

        Returns:
            menus.MenuItem: The newly created menu item.

        Raises:
            ValueError: If the menu item already exists.
        """
    db_menu_item = models.MenuItem(**menu_item.dict(), restaurant_id=restaurant_id)
    db.add(db_menu_item)

    try:
        db.commit()
        db.refresh(db_menu_item)
    except IntegrityError:
        db.rollback()
        raise ValueError("This menu already exists.")

    return menus.MenuItem.from_orm(db_menu_item)


def get_menu_items(db: Session, restaurant_id: int) -> list[menus.MenuItem]:
    """
        Get all menu items for the restaurant.

        Args:
            db (Session): The database session.
            restaurant_id (int): The ID of the restaurant.

        Returns:
            list[menus.MenuItem]: A list of menu items for the restaurant.
        """
    menu_items = db.query(models.MenuItem).filter(models.MenuItem.restaurant_id == restaurant_id).all()
    return [menus.MenuItem.from_orm(item) for item in menu_items]


def update_menu_item(db: Session, menu_item_id: int, menu_item: menus.MenuItemCreate) -> menus.MenuItem | None:
    """
        Updates the menu item.

        Args:
            db (Session): The database session.
            menu_item_id (int): The ID of the menu item.
            menu_item (menus.MenuItemCreate): The updated data for the menu item.

        Returns:
            menus.MenuItem | None: The updated menu item or None if the item was not found.
        """
    db_menu_item = db.query(models.MenuItem).filter(models.MenuItem.id == menu_item_id).first()

    if db_menu_item is None:
        return None

    for key, value in menu_item.dict().items():
        setattr(db_menu_item, key, value)

    db.commit()
    db.refresh(db_menu_item)
    return menus.MenuItem.from_orm(db_menu_item)


def delete_menu_item(db: Session, menu_item_id: int) -> menus.MenuItem | None:
    """
       Deletes a menu item.

       Args:
           db (Session): The database session.
           menu_item_id (int): The ID of the menu item.

       Returns:
           menus.MenuItem | None: The deleted menu item or None if the item was not found.
       """
    db_menu_item = db.query(models.MenuItem).filter(models.MenuItem.id == menu_item_id).first()

    if db_menu_item is None:
        return None

    db.delete(db_menu_item)
    db.commit()
    return menus.MenuItem.from_orm(db_menu_item)

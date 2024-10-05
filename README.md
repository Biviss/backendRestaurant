# Restaurant project

This project is a backend part of a website about restaurants and their menus built on FastAPI.

## Requirements

- Python 3.10
- MySQL

## Settings

1. Clone the repository and go to the project root folder:

   git clone https://github.com/Biviss/backendRestaurant.git
   cd backend

2. Create MySQL DB and create an .env file with database settings in the root folder of the project:

   SQLALCHEMY_DATABASE_URL=mysql+pymysql://<USERNAME>:<PASSWORD>@localhost/<DBNAME>

3. Build and run docker-compose.yml:

   docker-compose up --build


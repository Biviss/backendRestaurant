# Restaurant project

Цей проект є бекенд частиною сайту про ресторани та їх меню, побудованої на FastAPI.

## Вимоги

- Python 3.10
- MySQL

## Налаштування

1. Склонуйте репозиторій та зайдіть в корневу папку проекту:

   git clone https://github.com/Biviss/backendRestaurant.git
   cd backend

2. Створіть файл .env з налаштуваннями бази даних:

   SQLALCHEMY_DATABASE_URL=mysql+pymysql://<USERNAME>:<PASSWORD>@localhost/restaurant_db

3. Встановіть залежності:

   pip install -r requirements.txt

4. Запустіть проект:

   uvicorn app.main:app

5. Відкрийте браузер і перейдіть за адресою: http://localhost:8000/docs для перегляду API документації.

# Restaurant Kitchen Service (Portfolio Project)

A Django web app for managing a restaurant kitchen workflow:
- Cooks (custom user model)
- Dish types
- Ingredients
- Dishes with responsible cooks and ingredients

Built as a portfolio project (Taxi Service-like CRUD app + Bootstrap UI).

## Tech stack
- Python 3.11+
- Django 4.2
- SQLite (default)
- Bootstrap 5 (CDN)

## Features
- Authentication (login/logout)
- CRUD pages for: Cooks, Dish Types, Ingredients, Dishes
- Search + pagination on list pages
- Many-to-many relations:
  - Dish ↔ Cooks (responsible cooks)
  - Dish ↔ Ingredients
- Admin panel with helpful list displays

## Quick start

```bash
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open:
- App: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## DB diagram
See `docs/db_diagram.drawio` (editable in draw.io). 


## 🔐 Test Login Credentials

The project is deployed and доступен по адресу:

👉 https://restaurant-kitchen-manager-4x7p.onrender.com/accounts/login/?next=/

You can use the following test account to log in:

login: admin
password: admin12345

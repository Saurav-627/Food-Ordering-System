# Khaja Kham - Online Food Delivery System

A production-ready Django web application for food delivery with Admin, User, and Delivery Boy panels.

## Features
- **User Panel**: Browse foods, search, add to cart, checkout with Google Maps.
- **Delivery Boy Panel**: Dashboard, accept orders, navigate to delivery location.
- **Admin Panel**: Manage foods, categories, users, orders.
- **Recommendations**: Personalized suggestions, "People Also Ordered", and Smart Combos.
- **API**: REST API for mobile app integration.

## Setup

1. **Clone the repository**
2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate # Windows
   ```
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Environment Variables**
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key
   DEBUG=True
   GOOGLE_MAPS_API_KEY=your-google-maps-api-key
   ```
5. **Run Migrations**
   ```bash
   python manage.py migrate
   ```
6. **Seed Data**
   Populate the database with 25 Nepali foods and dummy users:
   ```bash
   python manage.py seed_dummy_data
   ```
7. **Train Recommendations**
   Generate similarity matrices:
   ```bash
   python manage.py train_recommendations
   ```
8. **Run Server**
   ```bash
   python manage.py runserver
   ```

## Users
- **Admin**: `admin` / `admin`
- **Delivery Boy**: `rider` / `rider`
- **User**: `user1` / `user1`

## Google Maps Integration
Ensure you have a valid Google Maps API Key with **Maps JavaScript API** and **Places API** enabled. Add it to `.env`.

## Deployment
- Set `DEBUG=False` in `.env`.
- Configure `ALLOWED_HOSTS`.
- Use PostgreSQL (install `psycopg2-binary` and update `DATABASES` in settings).
- Run `python manage.py collectstatic`.
- Use Gunicorn and Nginx.

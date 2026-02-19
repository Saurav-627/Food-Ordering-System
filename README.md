# 🍛 Khaja Kham - Smart Food Delivery Ecosystem

Khaja Kham is a high-performance, feature-rich Django web application designed for a modern food delivery business. It integrates **Machine Learning** for personalized recommendations and **OpenStreetMap** for real-time logistics, wrapped in a premium, responsive UI.

---

## 🚀 Core Features

-   **User Dashboard**: Professional catalog with search, categorization, and AJAX-powered cart.
-   **Rider/Delivery Panel**: Specialized interface for "Delivery Boys" to manage, track, and fulfill orders.
-   **Recommendation Engine**: Dual-layer ML using Collaborative Filtering (Cosine Similarity) and Market Basket Analysis.
-   **Dynamic Rating System**: Interactive 5-star rating system with text reviews and sentiment-based labeling.
-   **Geo-Logistics**: Integrated OpenStreetMap/Leaflet tracking (Privacy-focused, no API key costs).
-   **Order Lifecycle**: Real-time status updates from `Pending` -> `Confirmed` -> `On the way` -> `Completed`.

---

## 🛠️ Tech Stack

-   **Backend**: Django 4.0+, Python 3.10+
-   **Frontend**: Vanilla HTML5, Tailwind CSS (Custom Config), Lucide Icons
-   **Database**: SQLite (Development) / PostgreSQL (Production ready)
-   **ML Layer**: Scikit-Learn, NumPy, Pandas (Similarity Matrix Cache)
-   **Maps**: Leaflet.js & OpenStreetMap (OSM)

---

## 💻 Local Setup (Development)

1. **Clone & Enter Territory**
   ```bash
   git clone <repository-url>
   cd Khaja-Kham
   ```

2. **Setup Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # OR: venv\Scripts\activate (Windows)
   ```

3. **Install Core Engine**
   ```bash
   pip install -r requirements.txt
   ```

4. **Synchronize Database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Bootstrap Intelligence & Data**
   ```bash
   # Seed 25+ Nepali foods & test users
   python manage.py seed_dummy_data

   # Pre-compute Recommendation Similarity Matrix
   python manage.py train_recommendations
   ```

6. **Ignition**
   ```bash
   python manage.py runserver
   ```

---

## 📱 Running on Other Devices (Local Network)

To access Khaja Kham from your phone or another laptop on the same Wi-Fi:

1. **Find your Local IP**:
   - Linux/Mac: `ifconfig` (Look for `inet` under `en0` or `wlan0`)
   - Windows: `ipconfig` (Look for `IPv4 Address`)
   - *Example: 192.168.1.15*

2. **Run Server on All Interfaces**:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

3. **Access via Browser**:
   On your phone, go to `http://192.168.1.15:8000`

---

## 🏗️ Production Readiness Process (Deployment Checklist)

To move from "College Project" to "Real World Production":

### 1. Security (Critical)
- **Secret Key**: Move `SECRET_KEY` out of `settings.py` into Environment Variables.
- **Debug Mode**: Set `DEBUG = False`.
- **Allowed Hosts**: List your domain: `ALLOWED_HOSTS = ['khajakham.com.np', 'your-server-ip']`.

### 2. Database (PostgreSQL)
Install `psycopg2-binary` and update `DATABASES` in `settings.py` to point to a production-grade PostgreSQL instance.

### 3. Static & Media Management
- Run `python manage.py collectstatic`.
- Use **Nginx** to serve the `static_root` and `media_root`.
- Use **Gunicorn** or **Daphne** as the WSGI/ASGI server.

### 4. Recommendation Automation
Setup a **Cron Job** or **Celery Beat** to run `python manage.py train_recommendations` every hour/day to update suggestions based on new orders.

---

## 🔑 Test Credentials
- **Super Administrator**: `admin` / `admin`
- **Delivery Rider**: `rider` / `rider`
- **Customer Account**: `user1` / `user1`

---

## 📄 Documentation
Deep technical details, ERD/DFD diagrams, and architectural analysis can be found in `DOCUMENTATION.md` or via the `/presentation/` route on the live server.

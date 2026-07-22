# Online Shopping Management System (Amazon Clone)

A full-stack e-commerce demo built with **Python (Flask)**, **MySQL**, and
**HTML/CSS/JavaScript**, implementing the modules described in the project's
Software Requirements Specification: customer accounts, product catalog,
shopping cart, checkout & payments, reviews, and a full admin panel — backed
by a normalized MySQL database using joins, views, stored procedures,
triggers, functions, and indexes.

See `SETUP_GUIDE.md` for full step-by-step instructions to run this in VS Code.

## Quick Start

1. Install MySQL Server and VS Code (with the Python extension).
2. Create the database by running the files in `database/` in order (see
   SETUP_GUIDE.md for exact commands).
3. Create a virtual environment and install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and fill in your MySQL password.
5. Seed demo login passwords:
   ```
   python backend/seed.py
   ```
6. Run the app:
   ```
   python backend/app.py
   ```
7. Open http://127.0.0.1:5000 in your browser.

## Demo Logins
- Admin: `admin@shop.com` / `admin123`
- Customer: `john@example.com` / `password123`

## Project Structure
```
OnlineShoppingSystem/
├── frontend/          # static assets (css, js, images)
├── backend/           # Flask app (routes, models, services, templates)
├── database/          # schema, views, procedures, triggers, functions, sample data
├── requirements.txt
├── .env.example
└── SETUP_GUIDE.md
```

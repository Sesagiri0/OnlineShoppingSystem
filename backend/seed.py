"""
Run this ONCE after you've loaded schema.sql + sample_data.sql into MySQL.

It replaces the placeholder password hashes in the sample Users rows with
real Werkzeug hashes, so you can actually log in with:

  Admin:     admin@shop.com   / admin123
  Customer:  john@example.com / password123
  Customer:  jane@example.com / password123

Usage (from the project root, with your virtual environment active):
  python backend/seed.py
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from werkzeug.security import generate_password_hash
import mysql.connector
from backend.config import Config


def main():
    conn = mysql.connector.connect(
        host=Config.MYSQL_HOST,
        port=Config.MYSQL_PORT,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DATABASE,
    )
    cursor = conn.cursor()

    updates = [
        ("admin@shop.com", "admin123"),
        ("john@example.com", "password123"),
        ("jane@example.com", "password123"),
    ]

    for email, plain_password in updates:
        password_hash = generate_password_hash(plain_password)
        cursor.execute(
            "UPDATE Users SET password_hash = %s WHERE email = %s",
            (password_hash, email),
        )
        print(f"Updated password hash for {email}")

    conn.commit()
    cursor.close()
    conn.close()
    print("\nDone! You can now log in with the credentials listed in this file's docstring.")


if __name__ == "__main__":
    main()

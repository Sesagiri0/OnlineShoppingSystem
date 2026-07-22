"""
Application configuration.
Values are read from environment variables so you never have to hard-code
your database password. See the .env.example file in the project root.
"""

import os
from dotenv import load_dotenv

load_dotenv()  # loads variables from a .env file if present


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")

    MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
    MYSQL_PORT = int(os.environ.get("MYSQL_PORT", 3306))
    MYSQL_USER = os.environ.get("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "")
    MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE", "online_shopping")

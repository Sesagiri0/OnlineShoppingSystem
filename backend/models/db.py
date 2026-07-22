"""
Simple MySQL connection helper built on mysql-connector-python.
Every request gets its own connection which is closed automatically
by Flask's teardown hook (registered in app.py).
"""

import mysql.connector
from flask import g, current_app


def get_db():
    if "db" not in g:
        g.db = mysql.connector.connect(
            host=current_app.config["MYSQL_HOST"],
            port=current_app.config["MYSQL_PORT"],
            user=current_app.config["MYSQL_USER"],
            password=current_app.config["MYSQL_PASSWORD"],
            database=current_app.config["MYSQL_DATABASE"],
        )
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)


def query(sql, params=None, fetch=True, commit=False, many=False):
    """Small helper to run a query and optionally fetch results / commit."""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(sql, params or ())
    result = cursor.fetchall() if fetch else None
    if commit:
        db.commit()
    cursor.close()
    return result


def call_procedure(name, args=()):
    """Call a MySQL stored procedure and return any result sets it produces."""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.callproc(name, args)
    results = []
    for result in cursor.stored_results():
        results.extend(result.fetchall())
    db.commit()
    cursor.close()
    return results

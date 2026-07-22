from backend.models.db import query


def get_by_email(email):
    rows = query("SELECT * FROM Users WHERE email = %s", (email,))
    return rows[0] if rows else None


def get_by_id(user_id):
    rows = query("SELECT * FROM Users WHERE user_id = %s", (user_id,))
    return rows[0] if rows else None


def create_user(full_name, email, password_hash, phone, address, role="customer"):
    query(
        """INSERT INTO Users (full_name, email, password_hash, phone, address, role)
           VALUES (%s, %s, %s, %s, %s, %s)""",
        (full_name, email, password_hash, phone, address, role),
        fetch=False,
        commit=True,
    )


def update_password(user_id, new_hash):
    query(
        "UPDATE Users SET password_hash = %s WHERE user_id = %s",
        (new_hash, user_id),
        fetch=False,
        commit=True,
    )


def update_profile(user_id, full_name, phone, address):
    query(
        "UPDATE Users SET full_name = %s, phone = %s, address = %s WHERE user_id = %s",
        (full_name, phone, address, user_id),
        fetch=False,
        commit=True,
    )

from backend.models.db import query


def create_payment(order_id, method, amount, status="Pending"):
    query(
        """INSERT INTO Payments (order_id, payment_method, payment_status, amount)
           VALUES (%s, %s, %s, %s)""",
        (order_id, method, status, amount),
        fetch=False,
        commit=True,
    )


def mark_completed(order_id):
    query(
        "UPDATE Payments SET payment_status = 'Completed' WHERE order_id = %s",
        (order_id,),
        fetch=False,
        commit=True,
    )


def get_for_order(order_id):
    rows = query("SELECT * FROM Payments WHERE order_id = %s", (order_id,))
    return rows[0] if rows else None


def get_history_for_user(user_id):
    return query(
        """SELECT pay.* FROM Payments pay
           JOIN Orders o ON pay.order_id = o.order_id
           WHERE o.user_id = %s ORDER BY pay.payment_date DESC""",
        (user_id,),
    )

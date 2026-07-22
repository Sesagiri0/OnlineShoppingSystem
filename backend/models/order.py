from backend.models.db import query, call_procedure, get_db


def place_order_for_cart(user_id, cart_items, shipping_address):
    """
    cart_items: list of dicts {product_id, quantity}
    Uses the PlaceOrder stored procedure once per cart line so the
    reduce-stock trigger fires for every item, all items land on the
    same order, and a single order_id is returned.
    """
    db = get_db()
    order_id = None
    for item in cart_items:
        cursor = db.cursor()
        cursor.callproc(
            "PlaceOrder",
            (user_id, item["product_id"], item["quantity"], shipping_address, 0),
        )
        # Fetch OUT parameter
        for result in cursor.stored_results():
            result.fetchall()
        cursor.close()

    # Read back the most recent pending order id for this user
    rows = query(
        """SELECT order_id FROM Orders WHERE user_id = %s
           ORDER BY order_id DESC LIMIT 1""",
        (user_id,),
    )
    order_id = rows[0]["order_id"] if rows else None
    db.commit()
    return order_id


def get_order(order_id):
    rows = query("SELECT * FROM Orders WHERE order_id = %s", (order_id,))
    return rows[0] if rows else None


def get_order_items(order_id):
    return query(
        """SELECT oi.*, p.product_name, p.image_url
           FROM OrderItems oi JOIN Products p ON oi.product_id = p.product_id
           WHERE oi.order_id = %s""",
        (order_id,),
    )


def get_orders_for_user(user_id):
    return query(
        "SELECT * FROM Orders WHERE user_id = %s ORDER BY order_date DESC", (user_id,)
    )


def get_all_orders():
    return query(
        """SELECT o.*, u.full_name, u.email FROM Orders o
           JOIN Users u ON o.user_id = u.user_id
           ORDER BY o.order_date DESC"""
    )


def update_status(order_id, status):
    query(
        "UPDATE Orders SET status = %s WHERE order_id = %s",
        (status, order_id),
        fetch=False,
        commit=True,
    )


def cancel_order(order_id, user_id):
    query(
        "UPDATE Orders SET status = 'Cancelled' WHERE order_id = %s AND user_id = %s",
        (order_id, user_id),
        fetch=False,
        commit=True,
    )


def sales_report(start_date, end_date):
    return call_procedure("SalesReport", (start_date, end_date))

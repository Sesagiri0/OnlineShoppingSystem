from backend.models.db import query, call_procedure


def get_all(search=None, category_id=None):
    sql = "SELECT * FROM ProductDetails WHERE 1=1"
    params = []
    if search:
        sql += " AND product_name LIKE %s"
        params.append(f"%{search}%")
    if category_id:
        sql += " AND category_name = (SELECT category_name FROM Categories WHERE category_id = %s)"
        params.append(category_id)
    sql += " ORDER BY product_id DESC"
    return query(sql, tuple(params))


def get_by_id(product_id):
    rows = query("SELECT * FROM ProductDetails WHERE product_id = %s", (product_id,))
    return rows[0] if rows else None


def get_categories():
    return query("SELECT * FROM Categories ORDER BY category_name")


def get_reviews(product_id):
    return query(
        """SELECT r.*, u.full_name FROM Reviews r
           JOIN Users u ON r.user_id = u.user_id
           WHERE r.product_id = %s ORDER BY r.created_at DESC""",
        (product_id,),
    )


def add_review(product_id, user_id, rating, comment):
    query(
        "INSERT INTO Reviews (product_id, user_id, rating, comment) VALUES (%s, %s, %s, %s)",
        (product_id, user_id, rating, comment),
        fetch=False,
        commit=True,
    )


def add_product(name, description, price, stock, category_id, image_url):
    call_procedure("AddProduct", (name, description, price, stock, category_id, image_url))


def update_product(product_id, name, description, price, stock, category_id, image_url):
    query(
        """UPDATE Products SET product_name=%s, description=%s, price=%s,
           stock_quantity=%s, category_id=%s, image_url=%s WHERE product_id=%s""",
        (name, description, price, stock, category_id, image_url, product_id),
        fetch=False,
        commit=True,
    )


def delete_product(product_id):
    query("DELETE FROM Products WHERE product_id = %s", (product_id,), fetch=False, commit=True)


def restock(product_id, quantity_change):
    call_procedure("UpdateStock", (product_id, quantity_change))

"""
The shopping cart is kept in the browser session (server-side session,
signed cookie) as {product_id: quantity}. This keeps things simple and
needs no extra database table, matching a typical lightweight e-commerce
cart implementation.
"""

from flask import session
from backend.models.product import get_by_id


def get_cart():
    return session.get("cart", {})


def save_cart(cart):
    session["cart"] = cart
    session.modified = True


def add_item(product_id, quantity=1):
    cart = get_cart()
    key = str(product_id)
    cart[key] = cart.get(key, 0) + quantity
    save_cart(cart)


def update_item(product_id, quantity):
    cart = get_cart()
    key = str(product_id)
    if quantity <= 0:
        cart.pop(key, None)
    else:
        cart[key] = quantity
    save_cart(cart)


def remove_item(product_id):
    cart = get_cart()
    cart.pop(str(product_id), None)
    save_cart(cart)


def clear_cart():
    session.pop("cart", None)


def get_cart_details():
    cart = get_cart()
    items = []
    total = 0
    for product_id, qty in cart.items():
        product = get_by_id(int(product_id))
        if not product:
            continue
        subtotal = float(product["price"]) * qty
        total += subtotal
        items.append({"product": product, "quantity": qty, "subtotal": subtotal})
    return items, total

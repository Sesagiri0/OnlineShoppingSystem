from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from backend.services import cart_service

cart_bp = Blueprint("cart", __name__)


def _require_login():
    return "user_id" not in session


@cart_bp.route("/cart")
def view_cart():
    items, total = cart_service.get_cart_details()
    return render_template("cart.html", items=items, total=total)


@cart_bp.route("/cart/add/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    if _require_login():
        flash("Please log in to add items to your cart.", "error")
        return redirect(url_for("auth.login"))

    quantity = int(request.form.get("quantity", 1))
    cart_service.add_item(product_id, quantity)
    flash("Item added to cart.", "success")
    return redirect(request.referrer or url_for("product.list_products"))


@cart_bp.route("/cart/update/<int:product_id>", methods=["POST"])
def update_cart(product_id):
    quantity = int(request.form.get("quantity", 1))
    cart_service.update_item(product_id, quantity)
    return redirect(url_for("cart.view_cart"))


@cart_bp.route("/cart/remove/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id):
    cart_service.remove_item(product_id)
    flash("Item removed from cart.", "success")
    return redirect(url_for("cart.view_cart"))

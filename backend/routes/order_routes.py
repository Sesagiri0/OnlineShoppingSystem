from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from backend.services import cart_service
from backend.models import order as order_model
from backend.models import payment as payment_model
from backend.models import user as user_model

order_bp = Blueprint("order", __name__)


@order_bp.route("/checkout", methods=["GET", "POST"])
def checkout():
    if "user_id" not in session:
        flash("Please log in to checkout.", "error")
        return redirect(url_for("auth.login"))

    items, total = cart_service.get_cart_details()
    if not items:
        flash("Your cart is empty.", "error")
        return redirect(url_for("cart.view_cart"))

    user = user_model.get_by_id(session["user_id"])

    if request.method == "POST":
        shipping_address = request.form.get("shipping_address", user["address"])
        payment_method = request.form.get("payment_method", "Cash on Delivery")

        cart_items = [
            {"product_id": item["product"]["product_id"], "quantity": item["quantity"]}
            for item in items
        ]
        order_id = order_model.place_order_for_cart(
            session["user_id"], cart_items, shipping_address
        )
        order = order_model.get_order(order_id)
        payment_model.create_payment(order_id, payment_method, order["total_amount"])

        cart_service.clear_cart()
        return redirect(url_for("order.payment_page", order_id=order_id))

    return render_template("checkout.html", items=items, total=total, user=user)


@order_bp.route("/payment/<int:order_id>", methods=["GET", "POST"])
def payment_page(order_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    order = order_model.get_order(order_id)
    payment = payment_model.get_for_order(order_id)

    if request.method == "POST":
        # Simulated online payment confirmation
        payment_model.mark_completed(order_id)
        flash("Payment successful! Your order is now being processed.", "success")
        return redirect(url_for("order.order_history"))

    return render_template("payment.html", order=order, payment=payment)


@order_bp.route("/orders")
def order_history():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    orders = order_model.get_orders_for_user(session["user_id"])
    return render_template("order_history.html", orders=orders)


@order_bp.route("/orders/<int:order_id>")
def order_detail(order_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    order = order_model.get_order(order_id)
    items = order_model.get_order_items(order_id)
    payment = payment_model.get_for_order(order_id)
    return render_template("order_detail.html", order=order, items=items, payment=payment)


@order_bp.route("/orders/<int:order_id>/cancel", methods=["POST"])
def cancel_order(order_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    order_model.cancel_order(order_id, session["user_id"])
    flash("Order cancelled.", "success")
    return redirect(url_for("order.order_history"))

from functools import wraps
from datetime import date, timedelta

from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from backend.models import product as product_model
from backend.models import order as order_model
from backend.models.db import query

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if session.get("role") != "admin":
            flash("Admin access required.", "error")
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)
    return wrapped


@admin_bp.route("/")
@admin_required
def dashboard():
    stats = query(
        """SELECT
             (SELECT COUNT(*) FROM Users WHERE role='customer') AS total_customers,
             (SELECT COUNT(*) FROM Products) AS total_products,
             (SELECT COUNT(*) FROM Orders) AS total_orders,
             (SELECT COALESCE(SUM(total_amount),0) FROM Orders WHERE status <> 'Cancelled') AS total_revenue
        """
    )[0]
    low_stock = query("SELECT * FROM Products WHERE stock_quantity < 10")
    return render_template("admin/dashboard.html", stats=stats, low_stock=low_stock)


@admin_bp.route("/products")
@admin_required
def products():
    all_products = product_model.get_all()
    categories = product_model.get_categories()
    return render_template("admin/products.html", products=all_products, categories=categories)


@admin_bp.route("/products/add", methods=["POST"])
@admin_required
def add_product():
    product_model.add_product(
        request.form["product_name"],
        request.form.get("description", ""),
        float(request.form["price"]),
        int(request.form["stock_quantity"]),
        request.form.get("category_id") or None,
        request.form.get("image_url", ""),
    )
    flash("Product added.", "success")
    return redirect(url_for("admin.products"))


@admin_bp.route("/products/<int:product_id>/edit", methods=["POST"])
@admin_required
def edit_product(product_id):
    product_model.update_product(
        product_id,
        request.form["product_name"],
        request.form.get("description", ""),
        float(request.form["price"]),
        int(request.form["stock_quantity"]),
        request.form.get("category_id") or None,
        request.form.get("image_url", ""),
    )
    flash("Product updated.", "success")
    return redirect(url_for("admin.products"))


@admin_bp.route("/products/<int:product_id>/delete", methods=["POST"])
@admin_required
def delete_product(product_id):
    product_model.delete_product(product_id)
    flash("Product deleted.", "success")
    return redirect(url_for("admin.products"))


@admin_bp.route("/categories", methods=["GET", "POST"])
@admin_required
def categories():
    if request.method == "POST":
        query(
            "INSERT INTO Categories (category_name, description) VALUES (%s, %s)",
            (request.form["category_name"], request.form.get("description", "")),
            fetch=False, commit=True,
        )
        flash("Category added.", "success")
        return redirect(url_for("admin.categories"))

    all_categories = product_model.get_categories()
    return render_template("admin/categories.html", categories=all_categories)


@admin_bp.route("/customers")
@admin_required
def customers():
    all_customers = query("SELECT * FROM Users WHERE role = 'customer' ORDER BY created_at DESC")
    return render_template("admin/customers.html", customers=all_customers)


@admin_bp.route("/orders")
@admin_required
def orders():
    all_orders = order_model.get_all_orders()
    return render_template("admin/orders.html", orders=all_orders)


@admin_bp.route("/orders/<int:order_id>/status", methods=["POST"])
@admin_required
def update_order_status(order_id):
    order_model.update_status(order_id, request.form["status"])
    flash("Order status updated.", "success")
    return redirect(url_for("admin.orders"))


@admin_bp.route("/inventory", methods=["GET", "POST"])
@admin_required
def inventory():
    if request.method == "POST":
        product_model.restock(
            int(request.form["product_id"]), int(request.form["quantity_change"])
        )
        flash("Stock updated.", "success")
        return redirect(url_for("admin.inventory"))

    all_products = product_model.get_all()
    return render_template("admin/inventory.html", products=all_products)


@admin_bp.route("/payments")
@admin_required
def payments():
    all_payments = query(
        """SELECT pay.*, o.user_id, u.full_name FROM Payments pay
           JOIN Orders o ON pay.order_id = o.order_id
           JOIN Users u ON o.user_id = u.user_id
           ORDER BY pay.payment_date DESC"""
    )
    return render_template("admin/payments.html", payments=all_payments)


@admin_bp.route("/reports")
@admin_required
def reports():
    end = date.today()
    start = end - timedelta(days=30)
    report_rows = order_model.sales_report(start.isoformat(), end.isoformat())

    best_sellers = query(
        """SELECT p.product_name, SUM(oi.quantity) AS units_sold
           FROM OrderItems oi JOIN Products p ON oi.product_id = p.product_id
           GROUP BY p.product_name ORDER BY units_sold DESC LIMIT 5"""
    )
    top_customers = query(
        """SELECT u.full_name, SUM(o.total_amount) AS total_spent
           FROM Orders o JOIN Users u ON o.user_id = u.user_id
           WHERE o.status <> 'Cancelled'
           GROUP BY u.full_name ORDER BY total_spent DESC LIMIT 5"""
    )
    low_stock = query("SELECT * FROM Products WHERE stock_quantity < 10")
    revenue_by_category = query(
        """SELECT c.category_name, SUM(oi.quantity * oi.unit_price) AS revenue
           FROM OrderItems oi
           JOIN Products p ON oi.product_id = p.product_id
           JOIN Categories c ON p.category_id = c.category_id
           GROUP BY c.category_name ORDER BY revenue DESC"""
    )
    pending_orders = query("SELECT * FROM Orders WHERE status = 'Pending'")

    return render_template(
        "admin/reports.html",
        report_rows=report_rows,
        best_sellers=best_sellers,
        top_customers=top_customers,
        low_stock=low_stock,
        revenue_by_category=revenue_by_category,
        pending_orders=pending_orders,
    )

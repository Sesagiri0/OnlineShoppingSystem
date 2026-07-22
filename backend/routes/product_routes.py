from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from backend.models import product as product_model

product_bp = Blueprint("product", __name__)


@product_bp.route("/products")
def list_products():
    search = request.args.get("q", "").strip()
    category_id = request.args.get("category", "").strip()
    products = product_model.get_all(
        search=search or None, category_id=category_id or None
    )
    categories = product_model.get_categories()
    return render_template(
        "products.html", products=products, categories=categories,
        search=search, selected_category=category_id
    )


@product_bp.route("/products/<int:product_id>")
def product_detail(product_id):
    product = product_model.get_by_id(product_id)
    if not product:
        flash("Product not found.", "error")
        return redirect(url_for("product.list_products"))
    reviews = product_model.get_reviews(product_id)
    return render_template("product_detail.html", product=product, reviews=reviews)


@product_bp.route("/products/<int:product_id>/review", methods=["POST"])
def add_review(product_id):
    if "user_id" not in session:
        flash("Please log in to write a review.", "error")
        return redirect(url_for("auth.login"))

    rating = int(request.form["rating"])
    comment = request.form.get("comment", "").strip()
    product_model.add_review(product_id, session["user_id"], rating, comment)
    flash("Review submitted.", "success")
    return redirect(url_for("product.product_detail", product_id=product_id))


@product_bp.route("/")
def home():
    products = product_model.get_all()[:8]
    categories = product_model.get_categories()
    return render_template("index.html", products=products, categories=categories)

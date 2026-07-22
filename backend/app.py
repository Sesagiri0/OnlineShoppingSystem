import os
import sys

# Allow "backend.xxx" imports to work whether this file is run directly
# (python backend/app.py) or as a module (python -m backend.app)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask

from backend.config import Config
from backend.models import db as db_module
from backend.routes.auth_routes import auth_bp
from backend.routes.product_routes import product_bp
from backend.routes.cart_routes import cart_bp
from backend.routes.order_routes import order_bp
from backend.routes.admin_routes import admin_bp


def create_app():
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="../frontend",
        static_url_path="/static",
    )
    app.config.from_object(Config)

    db_module.init_app(app)

    app.register_blueprint(product_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(admin_bp)

    @app.context_processor
    def inject_globals():
        from flask import session
        from backend.services.cart_service import get_cart
        cart = get_cart()
        cart_count = sum(cart.values()) if cart else 0
        return dict(session=session, cart_count=cart_count)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)

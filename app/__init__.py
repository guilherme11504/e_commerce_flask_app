from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
from config import Config
from flask_cors import CORS
from flask_caching import Cache

db = SQLAlchemy()
cache = Cache()
scheduler = APScheduler()


def create_app():
    from app.models import Vendedor
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)
    
    db.init_app(app)
    cache.init_app(app, config={'CACHE_TYPE': 'SimpleCache'})
    scheduler.init_app(app)
    scheduler.start()


    # Registro de blueprints
    from app.routes.api.auth.views import auth_bp
    from app.routes.main.views import main_bp
    from app.routes.api.products.views import products_bp
    from app.routes.api.config.views import config_bp
    from app.routes.api.totem.views import totem_bp
    from app.routes.api.payments.views import payments_bp
    from app.routes.api.buyer.views import buyer_bp
    from app.routes.api.orders.views import orders_bp
    
    app.register_blueprint(buyer_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(config_bp)
    app.register_blueprint(totem_bp)
    app.register_blueprint(payments_bp)
    app.register_blueprint(orders_bp)
    return app

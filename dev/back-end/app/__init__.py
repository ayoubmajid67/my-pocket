from flask import Flask
from config import Config
from flask_cors import CORS


ls =5

# Import all the blueprints for different parts of the app
from app.routes.auth_routes import auth_bp
from app.routes.registerDemands_routes import registerDemands_bp
from app.routes.productsOffer_routes import productsOffer_bp
from app.routes.jobOffers_routes import jobOffers_bp
from app.routes.housingOffer_routes import housingOffer_bp
from app.routes.shoppingCard_routes import shoppingCard_bp
from app.routes.favorite_routes import favorite_bp
from app.routes.demands_routes import demands_bp
from app.routes.orders_routes import orders_bp
from app.routes.accounts_routes import accounts_bp
from app.routes.test_routes import tests_bp


from .db import db  # Import the db object

def create_app(config_class=Config):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_class)

    # Initialize the database with the app
    db.init_app(app)

    # Accessing the API_VERSION correctly from app.config
    API_VERSION = app.config['API_VERSION']

    # Register all blueprints
    app.register_blueprint(auth_bp, url_prefix=f'/api/{API_VERSION}/auth')
    app.register_blueprint(registerDemands_bp, url_prefix=f'/api/{API_VERSION}/registerDemands')
    app.register_blueprint(productsOffer_bp, url_prefix=f'/api/{API_VERSION}/productsOffers')
    app.register_blueprint(jobOffers_bp, url_prefix=f'/api/{API_VERSION}/jobsOffers')
    app.register_blueprint(housingOffer_bp, url_prefix=f'/api/{API_VERSION}/housingOffers')
    app.register_blueprint(shoppingCard_bp, url_prefix=f'/api/{API_VERSION}/shoppingCard')
    app.register_blueprint(favorite_bp, url_prefix=f'/api/{API_VERSION}/favorite')
    app.register_blueprint(demands_bp, url_prefix=f'/api/{API_VERSION}/demands')
    app.register_blueprint(orders_bp, url_prefix=f'/api/{API_VERSION}/orders')
    app.register_blueprint(accounts_bp, url_prefix=f'/api/{API_VERSION}/accounts')
    app.register_blueprint(tests_bp,url_prefix=f'/api/{API_VERSION}')

    return app

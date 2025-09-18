from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from .config import Config

# Global extensions

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
migrate = Migrate()


def create_app():
	app = Flask(__name__)
	app.config.from_object(Config)

	# Init extensions
	db.init_app(app)
	login_manager.init_app(app)
	migrate.init_app(app, db)

	# Register blueprints (placeholders; defined later)
	from .views.landing import landing_bp
	from .views.auth import auth_bp
	from .views.dashboard import dashboard_bp
	from .views.customers import customers_bp
	from .views.stock import stock_bp
	from .views.invoices import invoices_bp
	from .views.ledger import ledger_bp
	from .views.reports import reports_bp
	from .views.billing import billing_bp

	app.register_blueprint(landing_bp)
	app.register_blueprint(auth_bp)
	app.register_blueprint(dashboard_bp)
	app.register_blueprint(customers_bp, url_prefix="/customers")
	app.register_blueprint(stock_bp, url_prefix="/stock")
	app.register_blueprint(invoices_bp, url_prefix="/invoices")
	app.register_blueprint(ledger_bp, url_prefix="/ledger")
	app.register_blueprint(reports_bp, url_prefix="/reports")
	app.register_blueprint(billing_bp, url_prefix="/billing")

	with app.app_context():
		from . import models  # noqa: F401
		from .utils import seed_products_and_subtypes_if_empty  # noqa: E402
		seed_products_and_subtypes_if_empty()

	return app

from datetime import datetime
from enum import Enum
from flask_login import UserMixin
from . import db, login_manager


class StockAction(str, Enum):
	ADD = "Add"
	EDIT = "Edit"
	DEDUCT = "Deducted on Invoice"
	PRICE_UPDATED = "Price Updated"


class AdminUser(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True)
	password_hash = db.Column(db.String(255), nullable=False)
	is_active = db.Column(db.Boolean, default=True)

	def get_id(self):
		return str(self.id)


@login_manager.user_loader
def load_user(user_id):
	return AdminUser.query.get(int(user_id))


class Customer(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(120), nullable=False)
	address = db.Column(db.String(255))
	phone = db.Column(db.String(50))
	email = db.Column(db.String(120))
	notes = db.Column(db.Text)


class Product(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(120), nullable=False, unique=True)
	category = db.Column(db.String(120), nullable=False)


class StockItem(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
	sub_type = db.Column(db.String(120), nullable=True)
	quantity = db.Column(db.Float, default=0.0, nullable=False)
	unit = db.Column(db.String(20), default="kg", nullable=False)
	unit_price = db.Column(db.Float, default=0.0, nullable=False)
	product = db.relationship('Product', backref=db.backref('stock_items', lazy=True))

	__table_args__ = (
		db.UniqueConstraint('product_id', 'sub_type', name='uq_product_subtype'),
	)


class StockHistory(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
	sub_type = db.Column(db.String(120))
	action = db.Column(db.String(50), nullable=False)
	quantity = db.Column(db.Float, default=0.0)
	old_price = db.Column(db.Float)
	new_price = db.Column(db.Float)
	performed_by = db.Column(db.String(80))
	timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
	remarks = db.Column(db.String(255))
	product = db.relationship('Product')


class Invoice(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	invoice_number = db.Column(db.String(50), unique=True, nullable=False)
	date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
	customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
	grand_total = db.Column(db.Float, default=0.0)
	# Meta fields
	dispatch_type = db.Column(db.String(120))
	payment_terms = db.Column(db.String(255))
	ref_po_no = db.Column(db.String(120))
	due_date = db.Column(db.Date)
	customer_ntn = db.Column(db.String(120))
	customer_strn = db.Column(db.String(120))
	customer_tel = db.Column(db.String(120))
	customer_address = db.Column(db.String(255))
	account = db.Column(db.String(120))
	on_behalf_of = db.Column(db.String(120))
	contact_person = db.Column(db.String(120))
	contact_number = db.Column(db.String(120))
	# Totals
	subtotal = db.Column(db.Float, default=0.0)
	discount = db.Column(db.Float, default=0.0)
	gst_rate = db.Column(db.Float, default=0.0)
	gst_amount = db.Column(db.Float, default=0.0)
	amount_in_words = db.Column(db.String(255))

	customer = db.relationship('Customer')


class InvoiceItem(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'), nullable=False)
	product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
	sub_type = db.Column(db.String(120))
	uom = db.Column(db.String(20), default="KG")
	quantity = db.Column(db.Float, nullable=False)
	unit_price = db.Column(db.Float, nullable=False)
	tax = db.Column(db.Float, default=0.0)
	total = db.Column(db.Float, nullable=False)
	invoice = db.relationship('Invoice', backref=db.backref('items', lazy=True, cascade="all, delete-orphan"))
	product = db.relationship('Product')


class Payment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
	date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
	amount = db.Column(db.Float, nullable=False)
	method = db.Column(db.String(50))
	notes = db.Column(db.String(255))
	invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'))
	customer = db.relationship('Customer')
	invoice = db.relationship('Invoice', backref=db.backref('payments', lazy=True))


class FinanceEntry(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
	description = db.Column(db.String(255))
	debit_account = db.Column(db.String(120), nullable=False)
	credit_account = db.Column(db.String(120), nullable=False)
	amount = db.Column(db.Float, nullable=False)
	invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'))
	payment_id = db.Column(db.Integer, db.ForeignKey('payment.id'))

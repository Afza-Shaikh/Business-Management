from typing import Dict, List, Tuple
from . import db
from .models import Product, StockItem


BUTTER_SUBTYPES = [
	"Blend Butter",
	"Premium Butter",
	"Local Butter",
	"Baking Butter",
	"White Butter",
	"Yellow Butter",
	"Salted",
	"Unsalted",
	"Butterify",
]

DESI_GHEE_SUBTYPES = [
	"Blend Ghee",
	"Authentic Ghee",
]


def seed_products_and_subtypes_if_empty() -> None:
	"""Seed default products and sub-types if there are no products yet.
	Creates one StockItem per sub-type (quantity 0) so dropdowns always have options.
	"""
	if Product.query.count() > 0:
		return
	# Create products
	butter = Product(name="Butter", category="Dairy")
	desi_ghee = Product(name="Desi Ghee", category="Dairy")
	whipping = Product(name="Whipping Cream", category="Dairy")
	vinegar = Product(name="Vinegar", category="Condiment")
	yogurt = Product(name="Yogurt", category="Dairy")
	db.session.add_all([butter, desi_ghee, whipping, vinegar, yogurt])
	db.session.flush()
	# Create sub-type stock items
	for st in BUTTER_SUBTYPES:
		db.session.add(StockItem(product_id=butter.id, sub_type=st, quantity=0, unit_price=0))
	for st in DESI_GHEE_SUBTYPES:
		db.session.add(StockItem(product_id=desi_ghee.id, sub_type=st, quantity=0, unit_price=0))
	# Single standard entries for others
	db.session.add(StockItem(product_id=whipping.id, sub_type=None, quantity=0, unit_price=0))
	db.session.add(StockItem(product_id=vinegar.id, sub_type=None, quantity=0, unit_price=0))
	db.session.add(StockItem(product_id=yogurt.id, sub_type=None, quantity=0, unit_price=0))
	db.session.commit()


def build_grouped_stock_options() -> Dict[str, List[Tuple[int, str]]]:
	"""Return mapping: Product Name -> list of (stock_item_id, label) where label is sub-type or 'Standard'."""
	grouped: Dict[str, List[Tuple[int, str]]] = {}
	items = StockItem.query.join(Product, StockItem.product_id == Product.id).order_by(Product.name, StockItem.sub_type).all()
	for it in items:
		product_name = it.product.name if it.product else "Product"
		label = it.sub_type or "Standard"
		grouped.setdefault(product_name, []).append((it.id, label))
	return grouped

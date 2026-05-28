# backend/app/repository/__init__.py

# Expose your repositories cleanly from the folder level
from .customer_repo import CustomerRepository
from .orders_repo import OrderRepository
from .inventory_repo import InventoryRepository
from .bom_repo import BOMRepository
from .product_repo import ProductRepository

# Now anything outside this folder can import them all in one single line!
__all__ = [
    "CustomerRepository",
    "OrderRepository",
    "InventoryRepository",
    "BOMRepository",
    "ProductRepository"
]
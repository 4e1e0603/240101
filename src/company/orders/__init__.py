"""
The order service module.
"""

__all__ = [
    "OrderService",
    "Order",
    "Product",
    "User",
    "OrderRepository",
    "ProductRepository",
    "UserRepository",
]

from ._domain import User as User, Order as Order, Product as Product
from ._service import OrderService as OrderService
from ._storage import (
    UserRepository as UserRepository,
    ProductRepository as ProductRepository,
    OrderRepository as OrderRepository,
)

# ^^^^ Reimports: aliases are the trick to keep linters (Pylance) calm about unused imports.

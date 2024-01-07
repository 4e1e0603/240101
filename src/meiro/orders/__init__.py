"""
The order service module.
"""

__all__ = [
    "main",
    "OrderService",
    "Order",
    "Product",
    "User",
    "OrderRepository",
    "ProductRepository",
    "UserReposiotry",
]

from ._service import main as main, OrderService as OrderService
from ._domain import User as User, Order as Order, Product as Product
from ._schema import (
    UserRepository as UserRepository,
    ProductRepository as ProductRepository,
    OrderRepository as OrderRepository,
)

# ^^^^ Reimports: aliases are the trick to keep linters (Pylance) calm about unused imports.

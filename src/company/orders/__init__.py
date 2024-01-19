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

from company.orders._domain import User as User, Order as Order, Product as Product
from company.orders._service import OrderService as OrderService
from company.orders._storage import (
    UserRepository as UserRepository,
    ProductRepository as ProductRepository,
    OrderRepository as OrderRepository,
    create_schema as create_schema,
    delete_schema as delete_schema,
)

# ^^^^ Reimports: aliases are the trick to keep linters (Pylance) calm about unused imports.

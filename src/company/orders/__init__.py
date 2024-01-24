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
    "JSONError",
    "ConflictError",
]

from company.orders._domain import (
    User as User,
    Order as Order,
    Product as Product,
    UserID as UserID,
    ProductID as ProductID,
    OrderID as OrderID,
)

from company.orders._service import OrderService as OrderService

from company.orders._storage import (
    UserRepository as UserRepository,
    ProductRepository as ProductRepository,
    OrderRepository as OrderRepository,
    create_schema as create_schema,
    delete_schema as delete_schema,
    ConflictError as ConflictError,
)
from company.orders._common import JSONError as JSONError

# ^^^^ Reimports: aliases are the trick to keep linters (Pylance) calm about unused imports.

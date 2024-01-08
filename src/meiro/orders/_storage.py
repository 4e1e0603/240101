"""
This module contains database related code.
"""

from ._domain import User, Order, Product, AbstractRepository

__all__ = [
    "UserRepository",
    "OrderRepository",
    "ProductRepository",
]


class UserRepository(AbstractRepository[User]):
    def __init__(self, connection) -> None:
        self.connection = connection

    def save(self, entity: User) -> None:
        return NotImplemented

    def find(self, entity: User) -> User | None:
        return NotImplemented


class OrderRepository(AbstractRepository[Order]):
    def __init__(self, connection) -> None:
        self.connection = connection

    def save(self, entity: Order) -> None:
        return NotImplemented

    def find(self, entity: Order) -> Order | None:
        return NotImplemented


class ProductRepository(AbstractRepository[Product]):
    def __init__(self, connection) -> None:
        self.connection = connection

    def save(self, entity: Product) -> None:
        return NotImplemented

    def find(self, entity: Product) -> Product | None:
        return NotImplemented

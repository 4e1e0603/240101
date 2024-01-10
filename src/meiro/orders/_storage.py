"""
This module contains database related code such as implementation 
of repositories for each aggregate.
"""

import sys

from ._domain import User, Order, Product, AbstractRepository


__all__ = [
    "UserRepository",
    "OrderRepository",
    "ProductRepository",
]


class UserRepository(AbstractRepository[User]):
    """
    The repository for users.
    """

    def __init__(self, connection) -> None:
        self.connection = connection

    def save(self, aggregate: User) -> None:
        statement = "insert into users (id, name, city) values (?, ?, ?);"
        with self.connection as cursor:
            cursor.execute(statement, (aggregate.id, aggregate.name, aggregate.city))
        print(f"inserted {aggregate}", file=sys.stderr)  # DEBUG (remove)

    def find(self, aggregate: User) -> User | None:
        return NotImplemented


class OrderRepository(AbstractRepository[Order]):
    """
    The repository for orders.
    """

    def __init__(self, connection) -> None:
        self.connection = connection

    def save(self, aggregate: Order) -> None:
        return NotImplemented

    def find(self, aggregate: Order) -> Order | None:
        return NotImplemented


class ProductRepository(AbstractRepository[Product]):
    """
    The repository fo products.
    """

    def __init__(self, connection) -> None:
        self.connection = connection

    def save(self, aggregate: Product) -> None:
        return NotImplemented

    def find(self, aggregate: Product) -> Product | None:
        return NotImplemented

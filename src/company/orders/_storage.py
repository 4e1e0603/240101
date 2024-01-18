"""
This module contains database related code such as implementation 
of repositories for each aggregate. This is a infrastructure persistence layer.
"""


from ._domain import User, Order, Product
from ._shared import AbstractRepository


__all__ = [
    "UserRepository",
    "ProductRepository",
    "OrderRepository",
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
            cursor.execute(
                statement, (aggregate.identifier, aggregate.name, aggregate.city)
            )

    def find(self, aggregate: User) -> User | None:
        return NotImplemented

    def exists(self, aggregate: User) -> bool:
        statement = "select id from users where users.id = ?;"
        with self.connection as cursor:
            result = cursor.execute(statement, (aggregate.identifier,))
        return result.fetchone() is not None


class ProductRepository(AbstractRepository[Product]):
    """
    The repository fo products.
    """

    def __init__(self, connection) -> None:
        self.connection = connection

    def save(self, aggregate: Product) -> None:
        statement = "insert into products (id, name, price) values (?, ?, ?);"
        with self.connection as cursor:
            cursor.execute(
                statement, (aggregate.identifier, aggregate.name, aggregate.price)
            )

    def find(self, aggregate: Product) -> Product | None:
        return NotImplemented

    def exists(self, aggregate: Product) -> bool:
        statement = "select id from products where products.id = ?;"
        with self.connection as cursor:
            result = cursor.execute(statement, (aggregate.identifier,))
        return result.fetchone() is not None


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

    def exists(self, aggregate: User) -> bool:
        statement = "select id from orders where orders.id = ?;"
        with self.connection as cursor:
            result = cursor.execute(statement, (aggregate.identifier,))
        return result.fetchone() is not None

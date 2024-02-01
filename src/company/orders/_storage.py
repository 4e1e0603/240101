"""
This module contains database related code such as implementation 
of repositories for each aggregate. This is a infrastructure (persistence) layer.
"""

from typing import Iterator

from company.orders._domain import (
    User,
    Order,
    Product,
    OrderLine,
    UserID,
    ProductID,
    OrderID,
)
from company.orders._common import AbstractRepository, flatten, Timestamp


__all__ = [
    "UserRepository",
    "ProductRepository",
    "OrderRepository",
    "create_schema",
    "delete_schema",
    "ConflictError",
]


def create_schema(connection, schema_script: str) -> None:
    cursor = connection.cursor()
    cursor.executescript(schema_script)
    connection.commit()


def delete_schema(connection) -> None:
    cursor = connection.cursor()
    delete_tables = """
        drop table if exists order_lines;
        drop table if exists products;
        drop table if exists orders;
        drop table if exists users;
    """
    cursor.executescript(delete_tables)
    connection.commit()


class ConflictError(Exception):
    """Raised when the entity is already present."""


class UserRepository(AbstractRepository[User, UserID]):
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

    def find(self, aggregate_id: UserID) -> User | None:
        return NotImplemented

    def exists(self, aggregate_id: UserID) -> bool:
        statement = "select id from users where users.id = ?;"
        with self.connection as cursor:
            result = cursor.execute(statement, (aggregate_id,))
        return result.fetchone() is not None


class ProductRepository(AbstractRepository[Product, ProductID]):
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

    def find(self, aggregate_id: ProductID) -> Product | None:
        return NotImplemented

    def exists(self, aggregate_id: ProductID) -> bool:
        statement = "select id from products where products.id = ?;"
        with self.connection as cursor:
            result = cursor.execute(statement, (aggregate_id,))
        return result.fetchone() is not None


class OrderRepository(AbstractRepository[Order, OrderID]):
    """
    The repository for orders.
    """

    def __init__(self, connection) -> None:
        self.connection = connection

    def save(self, *aggregates: Order) -> None:
        with self.connection as cursor:
            # Create an order records.
            statement1 = "insert into orders (id, user_id, created) values (?, ?, ?)"
            cursor.executemany(
                statement1, ((_.identifier, _.user_id, _.created) for _ in aggregates)
            )
            # Create order line records.
            statement2 = "insert into order_lines (order_id, product_id, quantity) values (?, ?, ?)"
            order_lines = [
                [
                    (order.identifier, _.product_id, _.quantity)
                    for _ in order.order_lines
                ]
                for order in aggregates
            ]
            cursor.executemany(statement2, flatten(order_lines))

    def find(self, aggregate_id: OrderID) -> Order | None:
        return NotImplemented

    def exists(self, aggregate_id: UserID) -> bool:
        statement = "select id from orders where orders.id = ?;"
        with self.connection as cursor:
            found = cursor.execute(statement, (aggregate_id,))
        result = found.fetchone() is not None
        return result

    def find_between(self, since: Timestamp, till: Timestamp) -> Iterator[Order]:
        """
        Find orders in a specified range.

        :param since: ...
        :param till:  ...
        :returns: ...
        """
        statement = """
            select o.id,  o.created, o.user_id, l.product_id, l.quantity 
            from orders o join order_lines l on o.id = l.order_id 
            and o.created between ? and ? order by o.id"""
        with self.connection as cursor:
            found = cursor.execute(statement, (since, till)).fetchall()
            from itertools import groupby
            # This can be slow compared to better scheme e.g. denormalized view and query.
            # But point of this exercise is not to make fastest code possible.

            # Group values by a key e.g. `{(15, 1542373774, 0): [(11, 1), (9, 1)]`.
            #                                     order            order_lines
            for key, group in groupby(found, key=lambda x: (x[0], x[1], x[2])):
                order = Order(
                    identifier=key[0],
                    user_id=key[2],
                    created=key[1],
                    order_lines=[
                        OrderLine(product_id=item[-2], quantity=item[-1])
                        for item in group
                    ],
                )
                yield order

"""
This module contains a service layer related code.
"""

__all__ = ["OrderService"]


from pathlib import Path
from typing import Iterable, Iterator
from collections import Counter
import datetime
import json

from company.orders._domain import (
    User,
    UserRepository,
    Order,
    OrderLine,
    OrderRepository,
    Product,
    ProductRepository,
)
from company.orders._common import DateTimeRange, inform, JSONError, Any, DomainError
from company.orders._storage import ConflictError


class OrderService:
    """
    The order service contains methods for ordering products from customers.
    The :class:`OrderService` acts as an application facade, where each public
    method represents a use case defined by business requirements.

    :param user_repository: The user repository instance.
    :param order_repository: The order repository instance.
    :param product_repository: The product repository instance.

    TODO Send events to message dispatcher (bus).
    """

    def __init__(
        self,
        user_repository: UserRepository,
        order_repository: OrderRepository,
        product_repository: ProductRepository,
        logger=None,
    ) -> None:
        self._user_repository = user_repository
        self._order_repository = order_repository
        self.product_repository = product_repository
        self.logger = logger

    # ############################## Queries ############################## #

    def search_orders_by_date(
        self, since: datetime.datetime, till: datetime.datetime
    ) -> Iterator[Order]:
        """TODO"""
        date_time_range = DateTimeRange(since=since, till=till)
        result = self._order_repository.find_between(
            date_time_range.since_timestamp, date_time_range.till_timestamp
        )
        yield from result

    def search_users_with_most_products(self, connection, limit=3) -> Iterable[User]:
        # Use some `Provider`(protocol) instead of raw connection object.
        # It separates this method from knowledge of specific connection/storage type. 
        """
        Retrieve users with the highest number of purchased products in descending order.

        :param limit: The maximum of users to return.
        :returns: The users with the highest number of purchased products.
        """
        # DISCUSSION: Is it right to use raw SQL here? Should we provide some other class
        # as a dependency (e.g. provider) instead of concrete ODBC connection? This query
        # doesn't fit to any repository and complicates our "perfect" domain driven design :D
        # STATUS: It works but should be investigated more.
        with connection as cursor:
            found = cursor.execute(
                """       
                select orders.user_id, users.name, users.city, sum(order_lines.quantity) 
                from orders 
                join order_lines on order_lines.order_id = orders.id 
                join users on users.id = orders.user_id
                group by orders.user_id 
                order by sum(order_lines.quantity) 
                desc 
                limit ?;
            """,
                (limit,),
            ).fetchall()
            for item in found:
                yield User(*item[:-1])

    # ############################## Commands ############################# #

    def _parse_records(self, path) -> Iterator[Any]:  # better to use TypedDict for JSON
        """
        The helper method to read and parse records from provided JSONLine data file.
        This method can be easily  mocked for unit testing.

        :param path: A data file to be parsed.
        :raises :class:`JSONError`: when data can't be parsed as JSON.
        """
        with open(path, encoding="utf8") as file:
            for index, line in enumerate(file):
                try:
                    data = json.loads(line)
                    # TODO CHECK THAT JSON HAS PREDEFINED SCHEMA!
                    # We do not want any :class:`KeyError` errors later in the code!
                    yield data
                except ValueError as error:
                    raise JSONError(f"{index}: {line}") from error

    def batch_insert_orders(self, path: Path) -> None:
        """
        A batch insert from provided JSON-line dataset.

        :param path: A data file to be parsed.
        :raises:
            :class:`JSONError`: when data can't be parsed as JSON.
            :class:`DomainError`: when entity can't be created from data.
            :class:`ConflictError`: when an order already exists in database.
        """
        # Parse domain entities fro raw data.
        orders: list[Order] = []

        # NOTE Database writes should be transactional with rollback if something goes wrong.
        # We can use a unit of work pattern / context manager but we keep it simple for now.
        # We trust that attributes such as price for products does not change over dataset.
        # It should be true for provided dataset, but don't trust the input!
        for record in self._parse_records(path):
            # [1] Extract and save a new user.
            user = User(
                identifier=int(record["user"]["id"]),
                name=record["user"]["name"],
                city=record["user"]["city"],
            )
            if not self._user_repository.exists(user.identifier):
                self._user_repository.save(user)
                inform(self.logger, f"Saved {user}")

            # [2] Extract and save a new products.
            products = []
            for product_record in record["products"]:
                product = Product(
                    identifier=int(product_record["id"]),
                    name=product_record["name"],
                    price=product_record["price"],
                )
                if not self.product_repository.exists(product.identifier):
                    self.product_repository.save(product)
                    inform(self.logger, f"Saved {product}")
                products.append(product)

            # [3] Extract and save a new order.
            order_lines = [
                OrderLine(product_id=product.identifier, quantity=quantity)
                for product, quantity in Counter(products).items()
            ]

            result: Order | DomainError = Order.create(
                identifier=int(record["id"]),
                created=record["created"],
                user_id=user.identifier,
                order_lines=order_lines,
            )
            if isinstance(result, DomainError):
                raise result

            if self._order_repository.exists(result.identifier):
                raise ConflictError(f"Order {result.identifier} already exists")
            orders.append(result)
            # inform(self.logger, f"Created {order}")

        # [4] Store the orders as batch.
        self._order_repository.save(*orders)

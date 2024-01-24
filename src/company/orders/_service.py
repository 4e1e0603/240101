"""
This module contains a service layer related code.
"""

__all__ = ["OrderService"]


from pathlib import Path
from typing import Iterable, Iterator, TypeAlias
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
from company.orders._common import DateTimeRange, inform, JSONError
from company.orders._storage import ConflictError


JSON: TypeAlias = str


class OrderService:
    """The order service contains methods (use-cases) for ordering of products by users (customers).
    The class acts as an application facade.

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

    def search_orders_by_date_range(
        self, since: datetime.datetime, till: datetime.datetime
    ) -> Iterator[Order]:
        """TODO"""
        date_time_range = DateTimeRange(since=since, till=till)
        result = self._order_repository.find_between(
            date_time_range.since_timestamp, date_time_range.till_timestamp
        )
        yield from result

    def search_users_with_most_products(self, connection, limit=3) -> Iterable[User]:
        """
        Retrieve users with the highest number of purchased products in descending order.

        :param limit: The maximum of users to return.
        :returns: The users with the highest number of purchased products.
        """
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

    def _parse_records(self, path) -> Iterator[JSON]:
        """
        The helper method to read and parse records from provided JSONLine data file.
        This method can be easily  mocked for unit testing.

        :param path: A data file to be parsed.
        :raises :class:`JSONError`: when data can't be parsed as JSON.
        """
        with open(path, encoding="utf8") as file:
            lines = file.readlines()
        for index, line in enumerate(lines):
            try:
                yield json.loads(line)
            except ValueError as error:
                raise JSONError(line) from error

    def batch_insert_orders(self, path: Path) -> None:
        """
        A batch insert from provided JSON-line dataset.

        :param path: A data file to be parsed.
        :raises:
            :class:`JSONError`: when data can't be parsed as JSON.
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
                record["user"]["id"],
                name=record["user"]["name"],
                city=record["user"]["city"],
            )
            if not self._user_repository.exists(user):
                self._user_repository.save(user)
                inform(self.logger, f"Saved {user}")

            # [2] Extract and save a new products.
            products = []
            for product_record in record["products"]:
                product = Product(
                    product_record["id"],
                    name=product_record["name"],
                    price=product_record["price"],
                )
                if not self.product_repository.exists(product):
                    self.product_repository.save(product)
                    inform(self.logger, f"Saved {product}")
                products.append(product)

            # [3] Extract and save a new order.
            order_lines = [
                OrderLine(product_id=product.identifier, quantity=quantity)
                for product, quantity in Counter(products).items()
            ]
            order = Order(
                record["id"],
                created=record["created"],
                user_id=user.identifier,
                order_lines=order_lines,
            )
            if self._order_repository.exists(order):
                raise ConflictError(
                    f"Order {order.identifier} already exists"
                )  # TODO Create custom exception class.
            orders.append(order)
            # inform(self.logger, f"Created {order}")

        # [4] Store the orders as batch.
        self._order_repository.save(*orders)

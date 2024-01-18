"""
This module a service layer related code.

timetable
mon 01 01 14:15-14:50
sun 07 01 10:30-16:30
mon 08 01 21:00-
tue 09 01
wed 10 01
"""

__all__ = ["OrderService"]


from pathlib import Path
from typing import Iterable, TypeAlias
from collections import Counter

# Review: Some developers prefer basolute paths e.g. `meiro.orders._domain`

from ._domain import (
    User,
    Order,
    OrderLine,
    Product,
    UserRepository,
    ProductRepository,
    OrderRepository,
)
from ._shared import DateTimeRange


class JsonError(ValueError):
    """
    The exception raised when parsing JSON from text.
    Has better semantics then `` ValueError`` raise by :mod:`json`.
    """


JSON: TypeAlias = str


def inform(logger, message):
    """Print am informative message when the logger is provided, otherwise skip."""
    if logger is not None:
        logger.info(message)


class OrderService:
    """The order service contains methods (use-cases) for ordering of products by users (customers).
    The class acts as an application facade.

    :param user_repository: The user repository instance.
    :param order_repository: The order repository instance.
    :param product_repository: The product repository instance.
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

    def seach_orders(date_time_range: DateTimeRange) -> Iterable[Order]:
        return NotImplemented

    def search_users_by_ordered_products(limit) -> Iterable[User]:
        return NotImplemented

    def batch_insert(self, records: Iterable[JSON] | Path):
        """
        A batch insert from provided JSON-line dataset.

        :param records: TODO
        :raises: TODO
        """
        # NOTE This should probably be a transactional with rollaback for users and products tables.
        # => Use unit of work pattern in production.
        # Parse entities from raw data.
        for record in records:
            # Extract and save a new user.
            user = User(
                record["user"]["id"],
                name=record["user"]["name"],
                city=record["user"]["city"],
            )
            if not self._user_repository.exists(user):
                self._user_repository.save(user)
                inform(self.logger, f"Saved {user}")

            # Extract and save a new products.
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

            # Extract and save a new order.
            order_lines = [
                OrderLine(product_id=product.identifier, quantity=quantity)
                for product, quantity in Counter(products).items()
            ]

            order = Order(
                record["id"],
                created=record["created"],
                user=user.identifier,
                order_lines=order_lines,
            )

            if self._order_repository.exists(order):
                raise Exception(
                    "Order already exists"
                )  # TODO Create custom exception class.

            self._order_repository.save(order)

        # Store the orders in database.
        # Ensure that attributes for products and users does not change over dataset.
        # It should be true for provided dataset, but don't trust the input!

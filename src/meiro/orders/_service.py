"""
This module a service layer related code.

mo 01 01 14:15-14:50
su 07 01 10:30-16:30
mo 08 01 21:00-
"""

__all__ = ["OrderService"]


import json
from pathlib import Path
from typing import Iterable

# Review: Some developers prefer basolute paths e.g. `meiro.orders._domain`

from ._domain import User, Order, Product, Repository
from ._shared import DateTimeRange


class JsonError(ValueError):
    """
    The exception raised when parsing JSON from text.
    Has better semantics then `` ValueError`` raise by :mod:`json`.
    """


class OrderService:
    """The order service contains methods (use-cases) for ordering of products by users (customers).
    The class acts as an application facade.

    :param user_repository: The user repository instance.
    :param order_repository: The order repository instance.
    :param product_repository: The product repository instance.
    """

    def __init__(
        self,
        user_repository: Repository[User],
        order_repository: Repository[Order],
        product_repository: Repository[Product],
    ) -> None:
        self._user_repository = user_repository
        self._order_repository = order_repository
        self.product_repository = product_repository

    def seach_orders(date_time_range: DateTimeRange) -> Iterable[Order]:
        return NotImplemented

    def search_users_by_ordered_products(limit) -> Iterable[User]:
        return NotImplemented

    def batch_insert(self, file_path: str | Path):
        """
        A batch insert from provided JSON-line dataset.
        """
        with open(file_path, encoding="utf8") as file:
            lines = file.readlines()

        # TODO transactional
        orders: list[Order] = []
        for line in lines:
            try:
                data = json.loads(line)
            except ValueError as error:
                raise JsonError("Could not parse `{line}`") from error
            else:
                user = User(
                    id=data["user"]["id"],
                    name=data["user"]["name"],
                    city=data["user"]["city"],
                )
                products = [
                    Product(
                        id=product["id"], name=product["name"], price=product["price"]
                    )
                    for product in data["products"]
                ]
                order = Order(
                    id=data["id"],
                    created=data["created"],
                    user=user.id,
                    products=[p.id for p in products],
                )
                orders.append(order)

        for order in orders[:3]:
            print(order.products)
        # Store the orders in database.
        # Ensure that attributes for products and users does not change over datatset.
        # It shoukld be true for provided dataset, but don't trust the input!

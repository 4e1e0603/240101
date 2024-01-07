"""
This module a service layer related code.

mo 01 01 14:15-14:50
su 07 01 10:30-16:30 (2h break)
"""

__all__ = ["main", "OrderService"]


import argparse
import sys
from typing import Iterable
from pathlib import Path
from datetime import datetime
import json

# Review: Some developers prefer basolute paths e.g. `meiro.orders._domain`

from ._domain import User, Order, Product, Repository
from ._shared import DateTimeRange, JsonError
from ._schema import UserRepository, ProductRepository, OrderRepository


def main():
    """
    The main function for command line showcase.

    # print("Could not parse JSON object: {line}", file=sys.stderr) # Better to use logger for better control.
    # import sys
    # sys.exit(1)
    """
    print("--[SHOWCASE]--", file=sys.stderr)

    # engine = create_schema()

    parser = argparse.ArgumentParser("meiro-orders", "The orders service")
    parser.add_argument("--insert")

    options = parser.parse_args()

    service = OrderService(
        user_repository=UserRepository,
        order_repository=OrderRepository,
        product_repository=ProductRepository,
    )

    # Batch insert showcase
    # ---------------------------------------------------------------------- #
    if options.insert is not None:
        try:
            path = Path(options.insert.strip())
            service.batch_insert(file_path=path)
        except FileNotFoundError:
            print(f"File '{path}' could not be found.", file=sys.stderr)
            sys.exit(1)

    # Users showcase
    # ---------------------------------------------------------------------- #
    user1 = User(id=1, name="A", city="A")
    user2 = User(id=2, name="A", city="A")

    print(user1 == user2)  # expected == False

    # Products showcase
    # ---------------------------------------------------------------------- #
    product1 = Product(id=1, name="A", price=1)
    product2 = Product(id=2, name="A", price=1)

    print(product1 == product2)  # expected == False

    product3 = Product(id=1, name="B", price=2)  #
    print(product1 == product3)  # expected == True (same ID)

    # Orders showcase
    # ---------------------------------------------------------------------- #
    order1 = Order(id=1, user=user1.id, products=[product1.id], created=datetime.now())
    order2 = Order(
        id=1, user=user1.id, products=[product1.id, product2.id], created=datetime.now()
    )

    print(order1 == order2)


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
                raise JsonError from error
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

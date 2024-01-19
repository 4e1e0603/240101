"""
This module contains a service layer related code.
"""

__all__ = ["OrderService"]


from pathlib import Path
from typing import Iterable, Iterator, TypeAlias
from collections import Counter
import datetime

# Review: Some developers prefer absolute paths e.g. `company.orders._domain`

from ._domain import (
    User,
    Order,
    OrderLine,
    Product,
    UserRepository,
    ProductRepository,
    OrderRepository,
)
from ._shared import DateTimeRange, inform
from ._storage import ConflictError


JSON: TypeAlias = str


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

    def seach_orders_by_date_range(
        self, since: datetime.datetime, till: datetime.datetime
    ) -> Iterator[Order]:
        date_time_range = DateTimeRange(since=since, till=till)
        result = self._order_repository.find_between(
            date_time_range.since_timestamp, date_time_range.till_timestamp
        )
        yield from result

    def search_users_with_most_orders(limit) -> Iterable[User]:
        # select * from group by from database
        ...

    def batch_insert(self, records: Iterable[JSON] | Path) -> None:
        """
        A batch insert from provided JSON-line dataset.

        :param records: The records to be parsed.
        :raises: :class:`ConflictError`: when an order already exists.
        """
        # NOTE This should probably be a transactional with rollback if something goes wrong.
        # We can use a Unit of Work pattern / context manager.
        # We trust that attributes for products and users does not change over dataset.
        # It should be true for provided dataset, but don't trust the input!

        # Parse entities from raw data.
        orders: list[Order] = []
        for record in records:
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

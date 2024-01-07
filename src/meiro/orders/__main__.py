import argparse
import sys
from pathlib import Path
from datetime import datetime

from meiro.orders import (
    UserRepository,
    ProductRepository,
    OrderRepository,
    User,
    Order,
    Product,
    OrderService,
)


def main():
    """
    The main function for command line showcase.

    # print("Could not parse JSON object: {line}", file=sys.stderr)
    # ^^^ Better to use logger on module level for better control.
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

    # TODO Batch insert showcase
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

import argparse
import sys
from pathlib import Path


from meiro.orders import (
    UserRepository,
    ProductRepository,
    OrderRepository,
    OrderService,
)

from ._service import JsonError


def main():
    """
    The main function for command line showcase.


    # ^^^ Better to use logger on module level for better control.
    """
    print("--[SHOWCASE]--", file=sys.stderr)

    import sqlite3 as db

    schema_path = Path(Path(__file__).resolve().parents[1], "orders", "schema.sql")
    with open(schema_path, encoding="utf8") as schema:
        statements = schema.read()
        statements = [x.strip() for x in statements.split("----")]

    with db.connect("orders.db") as connection:
        cursor = connection.cursor()
        for statement in statements:
            cursor.execute(statement)
        cursor.execute("insert into users (id, name, city) values (1, 'name', 'city');")
        connection.commit()
        # connection.close()

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
        except JsonError:
            print("Could not parse line to JSON object", file=sys.stderr)

    # print(order1 == order2)

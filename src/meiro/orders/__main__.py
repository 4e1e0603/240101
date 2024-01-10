import argparse
import sys
from pathlib import Path
import sqlite3 as db

from meiro.orders import (
    User,
    UserRepository,
    ProductRepository,
    OrderRepository,
    OrderService,
)

from ._service import JsonError


def main():
    """
    The main function to demonstrate service functionality.
    """
    # Better to use logger on module level for better control.
    print("--[SHOWCASE]--", file=sys.stderr)

    schema_path = Path(Path(__file__).resolve().parents[1], "orders", "schema.sql")
    # Read, split, and clean statements (what about connection.executescript(sql_script) :D).
    with open(schema_path, encoding="utf8") as schema:
        statements = [
            x.strip() for x in schema.read().split("----") if not x.startswith("--")
        ]

    # Create database schema from parsed statements.
    with db.connect("orders.db") as connection:
        ur = UserRepository(connection)
        ur.save(User(99, "x", "y"))
        cursor = connection.cursor()
        for statement in statements:
            cursor.execute(statement)
        cursor.execute("insert into users (id, name, city) values (0, 'name', 'city');")
        connection.commit()

    # Define simple CLI interface.
    parser = argparse.ArgumentParser("meiro-orders", "The orders service")
    parser.add_argument("--insert")

    options = parser.parse_args()

    # Configure the application service.
    service = OrderService(
        user_repository=UserRepository,
        order_repository=OrderRepository,
        product_repository=ProductRepository,
    )

    # Showcase: the batch insert of data + use cases.
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

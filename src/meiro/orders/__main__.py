import argparse
import sys
from pathlib import Path
import sqlite3 as db
import json


import logging

from meiro.orders import (
    UserRepository,
    ProductRepository,
    OrderRepository,
    OrderService,
)

DATABASE_FILE = "orders.sqlite"


def main():
    """
    The main function to demonstrate service functionality.
    """
    # Better to use logger on module level for better control.
    logging.basicConfig(level=logging.INFO)

    # -----------------------------------------------------------------------
    # Define a simple CLI interface.
    # -----------------------------------------------------------------------
    parser = argparse.ArgumentParser("meiro-orders", "The orders service")
    parser.add_argument("--data", required=True)
    options = parser.parse_args()

    # -----------------------------------------------------------------------
    # Create database schema form the scripts.
    # -----------------------------------------------------------------------
    with db.connect(DATABASE_FILE) as connection:
        schema_path = Path(Path(__file__).resolve().parents[1], "orders", "schema.sql")
        # Crate a new tables.
        with open(schema_path, encoding="utf8") as schema:
            statements = schema.read()
        cursor = connection.cursor()
        cursor.executescript(statements)
        # Delete existing records.
        delete_tables = """
            delete from order_lines;
            delete from products;
            delete from orders;
            delete from users;
        """
        cursor.executescript(delete_tables)
        connection.commit()

    # Showcase: the batch insert of data + use cases.
    # -----------------------------------------------------------------------
    # Configure the application service.
    # -----------------------------------------------------------------------
    connection = db.connect(DATABASE_FILE)

    service = OrderService(
        user_repository=UserRepository(connection),
        order_repository=OrderRepository(connection),
        product_repository=ProductRepository(connection),
    )
    path = Path(options.data.strip())
    with open(path, encoding="utf8") as file:
        lines = file.readlines()

    error = (0, None)  # namedtuple?
    try:
        # We don't use comprehension to catch error for specific line.
        records = []
        for index, line in enumerate(lines):
            records.append(json.loads(line))
            print(f"Processed record {index + 1}/{len(lines)}", file=sys.stderr)
            sys.stderr.write("\033[F")

        service.batch_insert(records=records)
    except FileNotFoundError:
        error = (1, f"Could not find {path}")
    except ValueError:  # JsonError
        error = (2, f"Could not parse '{line}'")
    except KeyboardInterrupt:
        error = (3, "Interrupted by user")

    if error[0] == 0:
        print("--SUCCESS--")
    else:
        print(f"FAILURE {error[1]}", file=sys.stderr)

    sys.exit(error[0])

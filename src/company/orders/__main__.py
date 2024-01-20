import argparse
import sys
from pathlib import Path
import sqlite3 as db
import json

import datetime
import logging

from company.orders import (
    UserRepository,
    ProductRepository,
    OrderRepository,
    OrderService,
    create_schema,
    delete_schema,
)

DATABASE_FILE = "orders.sqlite"


def main():
    """
    The main function to demonstrate service functionality.
    """
    # Better to use logger on module level for better control.
    logging.basicConfig(level=logging.INFO)

    # -----------------------------------------------------------------------
    # Define a simple command line interface.
    # -----------------------------------------------------------------------
    parser = argparse.ArgumentParser("company-orders", "Some company orders service")
    parser.add_argument("--data", required=True)
    parser.add_argument("-v", "--verbose", action="store_true")

    options = parser.parse_args()

    LOGGER = None if not options.verbose else logging.getLogger(__name__)

    # -----------------------------------------------------------------------
    # Recreate database schema (this is only for showcase).
    # -----------------------------------------------------------------------
    with db.connect(DATABASE_FILE) as connection:
        schema_path = Path(Path(__file__).resolve().parents[1], "orders", "schema.sql")
        with open(schema_path, encoding="utf8") as schema:
            schema_script = schema.read()
        delete_schema(connection)
        create_schema(connection, schema_script)
        connection.commit()

    # -----------------------------------------------------------------------
    # Showcase: the batch insert of data + use cases.
    # -----------------------------------------------------------------------
    # Configure the main application service.
    connection = db.connect(DATABASE_FILE)

    service = OrderService(
        user_repository=UserRepository(connection),
        order_repository=OrderRepository(connection),
        product_repository=ProductRepository(connection),
        logger=LOGGER,
    )

    path = Path(options.data.strip())
    with open(path, encoding="utf8") as file:
        lines = file.readlines()

    # Exceute commands and handle errors.
    error = (0, None)  # TODO namedtuple(code, message)
    try:
        # ################################################################### #
        print("\n===[TASK 1]===\n", file=sys.stderr)
        # ################################################################### #
        # We don't use comprehension to catch error for specific line.

        records = []
        for index, line in enumerate(lines):
            records.append(json.loads(line))
            print(f"Processed records {index + 1}/{len(lines)}", file=sys.stderr)
            sys.stderr.write("\033[F")

        service.batch_insert_orders(records=records)

        # ################################################################### #
        print("\n\n===[TASK 2]===\n", file=sys.stderr)
        # ################################################################### #
        orders = service.search_orders_by_date_range(
            since=datetime.datetime(
                year=2018,
                month=11,
                day=16,
                hour=1,
                minute=29,
                second=4,  # an example taken from dataset
            ),
            till=datetime.datetime(
                year=2018,
                month=11,
                day=20,
                hour=10,
                minute=45,
                second=30,  # an example taken from dataset
            ),
        )
        for order in orders:
            print(
                f"Order(id={order.identifier},created='{datetime.datetime.fromtimestamp(order.created)}')",
                file=sys.stdout,
            )
            
        # ################################################################### #
        print("\n===[TASK 3]===\n", file=sys.stderr)
        # ################################################################### #
        top_users = service.search_users_with_most_products(limit = 5)
        print(top_users)

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

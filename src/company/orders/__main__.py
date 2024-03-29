import argparse
import sys
from pathlib import Path
import sqlite3 as db

import datetime
import logging

from company.orders import (
    UserRepository,
    ProductRepository,
    OrderRepository,
    OrderService,
    ConflictError,
    JSONError,
    delete_schema,
    create_schema,
    DomainError,
)


DATABASE_FILE = "orders.sqlite"
# This should be in some configuration file/object for production usage.


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

    # Exceute commands and handle errors.
    error_state = (0, None)  # TODO namedtuple(code, message)

    try:
        # ################################################################### #
        print("\n===[TASK 1]===\n", file=sys.stderr)
        # ################################################################### #
        path = Path(options.data.strip())
        print(f"Import records from file '{path}'...", file=sys.stderr)
        service.batch_insert_orders(path=path)
        print("\n===[DONE]===", file=sys.stderr)

        # ################################################################### #
        print("\n\n===[TASK 2]===\n", file=sys.stderr)
        # ################################################################### #
        date1 = datetime.datetime(2018, 11, 16, 1, 29, 4)
        date2 = datetime.datetime(2018, 11, 16, 10, 45, 30)
        print(f"Select orders between {date1} and {date2}...\n", file=sys.stderr)
        orders = service.search_orders_by_date(since=date1, till=date2)
        for order in orders:
            print(
                f"Order(id={order.identifier},created='{datetime.datetime.fromtimestamp(order.created)}')",
                file=sys.stdout,
            )
        print("\n===[DONE]===", file=sys.stderr)

        # ################################################################### #
        print("\n===[TASK 3]===\n", file=sys.stderr)
        # ################################################################### #
        limit = 5
        print(f"Select top {limit} users with most products...\n", file=sys.stderr)
        top_users = service.search_users_with_most_products(connection, limit=limit)
        for user in top_users:
            print(user)
        print("\n===[DONE]===", file=sys.stderr)

    except FileNotFoundError:
        error_state = (1, f"Could not find file {path}")
    except JSONError as error:
        error_state = (2, f"Could not parse record {error}")
    except KeyError as error:
        error_state = (3, f"Could not parse record because missing key {error}")
    except DomainError as error:
        error_state = (4, f"Could not create entity {error}")
    except ConflictError as error:
        error_state = (5, f"Record already exists {error}")
    except KeyboardInterrupt:
        error_state = (6, "Process exited by user")

    # TODO Catch other domain errors such as negative product price (ValueError/DomainError).

    if error_state[0] == 0:
        print("\n--SUCCESS--")
    else:
        print(f"\nFAILURE {error_state[0]}: {error_state[1]}", file=sys.stderr)

    sys.exit(error_state[0])

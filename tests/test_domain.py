from datetime import datetime

import pytest

from company.orders._domain import Order, Product, User, OrderLine

# ######################################################################### #
#                                   User                                    #
# ######################################################################### #


@pytest.mark.domain
def test_users_equality():
    lhs = User(1, "name1", "city1")
    rhs = User(1, "name2", "city2")
    assert lhs == rhs
    assert hash(lhs) == hash(rhs)


@pytest.mark.domain
def test_users_inequality():
    lhs = User(1, "name", "city")
    rhs = User(2, "name", "city")
    assert lhs != rhs
    assert hash(lhs) != hash(rhs)


# ######################################################################### #
#                                  Product                                  #
# ######################################################################### #


@pytest.mark.domain
def test_product_equality():
    lhs = Product(1, "name1", 2)
    rhs = Product(1, "name1", 2)
    assert lhs == rhs
    assert hash(lhs) == hash(rhs)


@pytest.mark.domain
def test_product_inequality():
    lhs = Product(1, "name", 1)
    rhs = Product(2, "name", 1)
    assert lhs != rhs
    assert hash(lhs) != hash(rhs)


# TODO def test_that_product_could_not_be_created_with_negative_price(): ...


# ######################################################################### #
#                                   Order                                   #
# ######################################################################### #


@pytest.mark.domain
def test_order_equality():
    lhs = Order(
        1,
        user_id=1,
        created=datetime(2023, 12, 1),
        order_lines=[OrderLine(1, 1), OrderLine(2, 2), OrderLine(3, 3)],
    )
    rhs = Order(
        1,
        user_id=2,
        created=datetime(2023, 12, 2),
        order_lines=[OrderLine(1, 3), OrderLine(2, 2), OrderLine(3, 1)],
    )
    assert lhs == rhs
    assert hash(lhs) == hash(rhs)


@pytest.mark.domain
def test_order_inequality():
    lhs = Order(
        1,
        user_id=1,
        created=datetime(2023, 12, 1),
        order_lines=[OrderLine(1, 1), OrderLine(2, 2), OrderLine(3, 3)],
    )
    rhs = Order(
        2,
        user_id=2,
        created=datetime(2023, 12, 2),
        order_lines=[OrderLine(1, 1), OrderLine(2, 2), OrderLine(3, 3)],
    )
    assert lhs != rhs
    assert hash(lhs) != hash(rhs)


def test_that_order_line_with_zero_quantity_is_forbidden():
    with pytest.raises(ValueError):
        Order(
            1,
            user_id=1,
            created=datetime(2023, 12, 1),
            order_lines=[OrderLine(1, 0)],
        )


def test_that_order_line_with_negative_quantity_is_forbidden():
    with pytest.raises(ValueError):
        Order(
            1,
            user_id=1,
            created=datetime(2023, 12, 1),
            order_lines=[OrderLine(1, -1)],
        )


@pytest.mark.domain
def test_order_factory_method_returns_success():
    result = Order.create(
        1,
        user_id=1,
        created=datetime(2023, 12, 1),
        order_lines=[OrderLine(1, 1)],
    )
    assert isinstance(result, Order)


# FIXME
# @pytest.mark.domain
# def test_order_factory_method_returns_failure():
#     result = Order.create(1,user_id=1, created=datetime(2023, 12, 1),order_lines=[OrderLine(1, -99)])
#     assert True
#     # assert isinstance(result, ValueError)

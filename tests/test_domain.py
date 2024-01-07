from datetime import datetime

import pytest

from meiro.orders._domain import Order, Product, User


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


@pytest.mark.domain
def test_order_equality():
    lhs = Order(1, user=1, created=datetime(2023, 12, 1), products=[1, 2, 3])
    rhs = Order(1, user=2, created=datetime(2023, 12, 2), products=[4, 5, 6])
    assert lhs == rhs
    assert hash(lhs) == hash(rhs)


@pytest.mark.domain
def test_order_inequality():
    lhs = Order(1, user=1, created=datetime(2023, 12, 1), products=[1, 2, 3])
    rhs = Order(2, user=1, created=datetime(2023, 12, 1), products=[1, 2, 3])
    assert lhs != rhs
    assert hash(lhs) != hash(rhs)

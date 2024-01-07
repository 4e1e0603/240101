from datetime import datetime
from meiro.orders._domain import Order, Product, User


def test_user_equality_laws():
    lhs = User(1, "A", "C")
    rhs = User(1, "B", "D")
    assert lhs == rhs
    assert hash(lhs) == hash(rhs)


def test_product_equality_laws():
    lhs = Product(1, "A", 1)
    rhs = Product(1, "B", 2)
    assert lhs == rhs
    assert hash(lhs) == hash(rhs)


def test_order_equality_laws():
    lhs = Order(1, user=1, created=datetime(2023, 12, 1), products=[1, 2, 3])
    rhs = Order(1, user=2, created=datetime(2023, 12, 1), products=[1, 2, 3])
    assert lhs == rhs
    assert hash(lhs) == hash(rhs)

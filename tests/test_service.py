import pytest

from typing import Generic, TypeVar

from company.orders import User, Product, Order, OrderService
from company.orders._storage import ConflictError

# Create fake repositories to be injected to initializer of service.

T = TypeVar("T")


class FakeRepository(Generic[T]):
    def __init__(self) -> None:
        self._storage = {}

    def save(self, aggregate) -> None:
        if self.exists(aggregate):
            raise ConflictError
        self._storage[aggregate] = aggregate

    def find(self, aggregate) -> User | None:
        return self._storage.get(aggregate, None)

    def exists(self, aggregate) -> bool:
        return aggregate in self._storage


class FakeUserRepository(FakeRepository[User]):
    pass


class FakeProductRepository(FakeRepository[Product]):
    pass


class FakeOrderRepository(FakeRepository[Order]):
    pass


def test_fake_repository():
    repo = FakeUserRepository()
    repo.save(User(1, 1, 1))
    assert repo.exists(User(1, 1, 1))


@pytest.fixture
def order_service():
    service = OrderService(
        user_repository=FakeUserRepository(),
        product_repository=FakeProductRepository(),
        order_repository=FakeOrderRepository(),
    )
    return service


@pytest.mark.skip
def test_order_service_method1(order_service):
    return NotImplemented


@pytest.mark.skip
def test_order_service_method2(order_service):
    return NotImplemented

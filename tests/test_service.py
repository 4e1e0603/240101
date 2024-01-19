import pytest

# Create fake repositories to be injected to initializer of service.
#  ...


@pytest.fixture
def order_service():
    """Create an service instance to test with fake dependencies."""
    return NotImplemented


def test_order_service_method1(order_service):
    return NotImplemented


def test_order_service_method2(order_service):
    return NotImplemented

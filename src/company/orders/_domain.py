"""
This module a domain layer related code. 

“There are only two industries that refer to their customers as ‘users’, 
one is of course IT, the other is the illegal drugs trade…” — Edward Tufte
"""

__all__ = [
    "User",
    "Order",
    "Product",
    "UserRepository",
    "OrderRepository",
    "ProductRepository",
    "DomainError",
]


from dataclasses import dataclass
from typing import TypeAlias, Iterable, Self, Iterator
from datetime import datetime

from company.orders._shared import Entity, Timestamp, Repository


class DomainError(Exception):
    """
    Represents an exception raised in domain layer.
    """


# ########################################################################### #

UserID: TypeAlias = int


class User(Entity[UserID]):
    """
    The custommer domain model.
    """

    def __init__(self, identifier: int, name: str, city: str) -> None:
        if identifier < 0:
            raise ValueError("An identifier cannot be a negative number.")
        super().__init__(identifier=identifier)
        self._name = name
        self._city = city

    @property
    def name(self) -> str:
        """
        Returns a user's name.

        :returns: a user's name.
        """
        return self._name

    @property
    def city(self) -> str:
        """
        Returns a user's city name.

        :returns: a user's city name.
        """
        return self._city

    # We can implement this with setters, but I prefer immutable instances.
    # We don't care if an attribute is the same as an original. We always return a new instance.

    def change_name(self, name: str) -> Self:
        """
        Change the users's name.

        :param name: The new user's name.
        """
        return type(self)(identifier=self.identifier, name=name, city=self.city)

    def change_city(self, city: str) -> Self:
        """
        Change the users's city.

        :param name: The new user's city.
        """
        return type(self)(identifier=self.identifier, name=self.name, city=city)


class UserRepository(Repository[User]):
    """
    The repository protocol for users.
    """


# ########################################################################### #

ProductID: TypeAlias = int


class Product(Entity[ProductID]):
    """
    The product domain model.

    The price should be of some special `Money` or `Decimal` type.
    Never ever use floats!
    """

    def __init__(
        self,
        identifier: ProductID,
        name: str,
        price: int,
    ):
        if identifier < 0:
            raise ValueError("An identifier cannot be a negative number.")
        super().__init__(identifier=identifier)
        self._name = name
        self._price = price

    @property
    def name(self) -> str:
        """
        :returns: a product's name.
        """
        return self._name

    @property
    def price(self) -> str:
        """
        :returns: a product's price.
        """
        return self._price


class ProductRepository(Repository[Product]):
    """
    The repository protocol for products.
    """


# ########################################################################### #

OrderID: TypeAlias = int


@dataclass(frozen=True, slots=True)
class OrderLine:
    """
    The order lines for specific order.
    """

    product_id: ProductID
    quantity: int = 1


class Order(Entity[OrderID]):
    """
    The order domain model.

    Contains 1 user and 1..N order lines.

    ..note: You can probably change products (insert, remove) or
    assign the order to a different user. You cannot change `id` and
    `created` attributes. Can the order have a 0 products?
    """

    def __init__(
        self,
        identifier: OrderID,
        user_id: UserID,
        order_lines: Iterable[OrderLine],
        created: datetime | Timestamp,
    ) -> None:
        if identifier < 0:
            raise ValueError("Identifier cannot be a negative number")
        super().__init__(identifier=identifier)
        self._user_id = user_id
        self._created = (
            datetime.timestamp(created) if isinstance(created, datetime) else created
        )
        self._order_lines = frozenset(order_lines)

    @property
    def user_id(self) -> UserID:
        return self._user_id

    @property
    def created(self) -> Timestamp:
        return self._created

    @property
    def order_lines(self) -> Iterable[OrderLine]:
        return tuple(self._order_lines)

    @property
    def _products(self) -> Iterable[ProductID]:
        return sorted([_.product_id for _ in self.order_lines])

    def has_product(self, product_id: ProductID) -> bool:
        return product_id in self._products

    def has_same_products(self, other: Self) -> bool:
        return self._products == other._products

    # TODO Future work
    # @classmethod
    # def create(
    #     cls: Type[Self],
    #     id: OrderID,
    #     user: UserID,
    #     created: datetime | Timestamp,
    #     products: ProductID
    #     ) -> Type[Self]:
    #     """
    #     Create a new order with this factory method instead of initializer.
    #     """
    #     return cls(identifier=id, created = created, user=user, *products)


class OrderRepository(Repository[Order]):
    """
    The repository protocol for orders.
    """

    def find_between(self, since: Timestamp, till: Timestamp) -> Iterator[Order]:
        """
        Find orders in a specified range.

        :param since: ...
        :param till:  ...
        :returns: ...
        """
        return NotImplemented

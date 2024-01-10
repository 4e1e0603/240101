"""
This module a domain layer related code. 

“There are only two industries that refer to their customers as ‘users’, 
one is of course IT, the other is the illegal drugs trade…” — Edward Tufte
"""

__all__ = [
    "User",
    "Order",
    "Product",
    "DomainError",
    "Repository",
    "AbstractRepository",
]

from abc import ABC, abstractmethod
from typing import TypeAlias, Iterable, Self, Generic, TypeVar, Protocol
from datetime import datetime

from ._shared import Entity, Timestamp
# Review: Some developers prefer absolute paths e.g. `meiro.orders._shared`.


class DomainError(Exception):
    """
    Represents an exception raised in domain layer.
    """


UserID: TypeAlias = int  # Mypy doesn't yet implements the *type statement* (3.12).
ProductID: TypeAlias = int
OrderID: TypeAlias = int


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
        :returns: a user's name.
        """
        return self._name

    @property
    def city(self) -> str:
        """
        :returns: a user's city.
        """
        return self._city

    # We can implement this with setters, but I prefer immutable instances.
    # We don't care if an attribute is the same as an original. We always return a new instance.

    def change_name(self, name: str) -> Self:
        """
        Change the users's name.

        :param name: The new user's name.
        """
        return type(self)(id=self.id, name=name, city=self.city)

    def change_city(self, city: str) -> Self:
        """
        Change the users's city.

        :param name: The new user's city.
        """
        return type(self)(id=self.id, name=self.name, city=city)


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
        return self._city


class Order(Entity[OrderID]):
    """
    The order domain model.

    Contains 1 User and 1..N products.

    ..note: You can probably change products (insert, remove) or
    assign the order to a different user. You cannot change `id` and
    `created` attributes. Can the order have a 0 products?

    e.g.
    {
        "id": 21,
        "created": 1538444645,
        "products": [{"id": 2, "name": "Product C", "price": 140}],
        "user": {"id": 0, "name": "User A", "city": "Prague"}
    }
    """

    def __init__(
        self,
        identifier: OrderID,
        user: UserID,
        created: datetime | Timestamp,
        products: Iterable[ProductID],
    ) -> None:
        if identifier < 0:
            raise ValueError("Identifier cannot be a negative number")
        if len(products) == 0:
            raise ValueError("Products cannot be and empty collection")

        super().__init__(identifier=identifier)
        self._user = user
        self._created = (
            datetime.timestamp(created) if isinstance(created, datetime) else created
        )
        self._products = frozenset(products)

    # @classmethod
    # def create(
    #     cls: Type[Self],
    #     id: OrderID,
    #     user: UserID,
    #     created: datetime | Timestamp,
    #     products: ProductID
    #     ) -> Type[Self]:
    #     """
    #     Create a new order with this factory method.
    #     """
    #     return cls(id=id, created = created, user=user, *products)

    @property
    def user(self) -> UserID:
        return self._user

    @property
    def created(self) -> Timestamp:
        return self._created

    @property
    def products(self) -> Iterable[ProductID]:
        return sorted(tuple(self._products))

    def has_product(self, product_id: ProductID) -> bool:
        return product_id in self.products

    def has_same_products(self, other: Self) -> bool:
        return self.products == other.products

    def remove_product(self, product_id: ProductID) -> Self:
        if not self.has_product(product_id):
            raise DomainError(f"Product {product_id} is not present")
        return type(self)(
            id=self.id,
            created=self.created,
            user=self.user,
            *self._products.difference(product_id),
        )

    def insert_product(self, product_id: ProductID) -> Self:
        return NotImplemented

    def assign_to_user(user_id: UserID) -> Self:
        return NotImplemented


EntityType = TypeVar("EntityType", bound=Entity)


class Repository(Generic[EntityType], Protocol):
    """
    Save and find entitiy in the repository.
    """

    def save(self, entity) -> None:
        """
        Save the entity to the storage.

        :param entity: The entity to save.
        """

    def find(self, entity) -> EntityType | None:
        """
        Find the entity in the storage.

        :param entity: The entity to find.
        :returns: The found entity or `None`.
        """


class AbstractRepository(ABC, Generic[EntityType]):
    def __init__(self, connection) -> None:
        self.connection = connection

    @abstractmethod
    def save(entity) -> None:
        """
        Save the entity to the storage.

        :param entity: The entity to save.
        """

    @abstractmethod
    def find(entity) -> EntityType | None:
        """
        Find the entity in the storage.

        :param entity: The entity to find.
        :returns: The found entity or `None`.
        """

"""
This module contains a shared code and general abstractions.
"""

# mypy: disable-error-code=empty-body
# Mypy is not smart enough to figure out that your decorator calls `abc.abstractmethod`

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Protocol, TypeAlias
from dataclasses import dataclass
from datetime import datetime


__all__ = [
    "Entity",
    "Repository",
    "AbstractRepository",
    "Timestamp",
    "DateTimeRange",
    "Name",
    "Identifiable",
]


@dataclass(frozen=True, slots=True)
class DateTimeRange:
    """
    The value object represents the date and time range.
    """

    lower_bound: datetime
    upper_bound: datetime

    def __post_init__(self) -> None:
        """check the boundaries lower >= upper"""


@dataclass(frozen=True, slots=True)
class Name:
    value: str

    def __post_init(self) -> None:
        if self.value == "":
            raise ValueError("Empty string is not allowed")


Timestamp: TypeAlias = float
"""The timestamp alias for primitive float value."""
# type Timestamp = float
# NOTE PEP 695 type aliases are not yet supported by Mypy (2023-01-08)


Identifier = TypeVar("Identifier")
"""Some unique entitie's identifier."""


class Identifiable(Protocol, Generic[Identifier]):
    @property
    def identifier(self) -> Identifier:
        """The entitiy unique identifier."""


class Entity(ABC, Generic[Identifier]):
    """
    An entity object in the terms of Doman-driven design.

    :param identifier:
    """

    def __init__(self, identifier: Identifier):
        self._identifier = identifier

    @property
    def identifier(self) -> Identifier:
        return self._identifier

    def __eq__(self, other: object) -> bool:
        return isinstance(other, type(self)) and self.identifier == other.identifier

    def __hash__(self) -> int:
        return hash((type(self), self.identifier))

    def __str__(self) -> str:
        import inspect

        fields = inspect.getmembers(type(self), lambda a: not (inspect.isroutine(a)))
        fields = [
            f"{f[0]}={getattr(self, str(f[0]))}"
            for f in fields
            if (not f[0].startswith("_")) and (not f[0].startswith("__"))
        ]
        return f"{type(self).__name__}({",".join(fields)})"

    __repr__ = __str__  # Maybe prefer not to override this.

    # NOTE The transfer layer (data transfer object) related method.
    # Maybe use a standalone :class:`JsonEncoder` in DTO module.
    # def to_json(self): return NotImplemented


EntityType = TypeVar("EntityType", bound=Entity)


class Repository(Generic[EntityType], Protocol):
    """
    The aggregate root entitiy repository protocol.
    """

    def save(self, aggregate) -> None:
        """
        Save the aggregate root entity to the storage.

        :param aggregate: The entity to save.
        """

    def find(self, aggregate) -> EntityType | None:
        """
        Find the unique entity matching the predicate.

        The predicate must match exactly one or zero entity.

        :param aggregate: The entity to find.
        :param aggregate: The entity to find.
        :returns: The found entity or `None`.
        """

    # def find_all(
    #     self, aggregate, predicate: Callable[[EntityType], bool]
    # ) -> Iterable[EntityType]:
    #     """Find all entities matching the predicate."""

    def exists(self, aggregate) -> bool:
        """
        Check if aggregate  root entity exists in storage.

        :param aggregate: The entity to find.
        :returns: The `True` if found, otherwise `False`.
        """


class AbstractRepository(ABC, Generic[EntityType]):
    """
    The aggregate root entitiy repository abstract base class.

    The repository is not responsible for managing connection.
    The connection pool is recommended. The implementation can
    be modified e.g add context manager but wee keep it simple
    now.

    :param connection: A database connection object.
    """

    def __init__(self, connection) -> None:
        self.connection = connection

    @abstractmethod
    def save(self, aggregate) -> None:
        """
        Save the entity to the storage.

        :param aggregate: The entity to save.
        """

    @abstractmethod
    def find(
        self,
        aggregate,
    ) -> EntityType | None:
        """
        Find the unique entity matching the predicate.

        The predicate must match exactly one or zero entity.

        :param aggregate: The entity to find.
        :param aggregate: The entity to find.
        :returns: The found entity or `None`.
        """

    @abstractmethod
    def exists(self, aggregate) -> bool:
        """
        Check if aggregate  root entity exists in storage.

        :param aggregate: The entity to find.
        :returns: The `True` if found, otherwise `False`.
        """

"""This module contains code shared between modules and packages.
This can be reused between projects in the future.
"""

# mypy: disable-error-code=empty-body
# Mypy is not smart enough to figure out that your decorator calls `abc.abstractmethod`

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Protocol, TypeAlias, Any, Hashable
from dataclasses import dataclass
from datetime import datetime
import inspect

__all__ = [
    "Entity",
    "Repository",
    "AbstractRepository",
    "Timestamp",
    "DateTimeRange",
    "Name",
    "Identifiable",
    "flatten",
    "inform",
    "JSONError",
    "Event",
    "Command",
    "JSON",
]

JSON: TypeAlias = str


def inform(logger, message) -> None:
    """Print the info message when the logger is provided, otherwise skip.
    :param: The logger instance.
    :param: The message to print.
    """
    if logger is not None:
        logger.info(message)


def flatten(xss: list[list[Any]]) -> list[Any]:
    """Flatten the given list.

    :param xss: The list of lists.
    :return: the flattened list of items.
    """
    return [x for xs in xss for x in xs]


class JSONError(ValueError):
    """
    The exception raised when parsing JSON from text.
    Has better semantics then :class:`ValueError` raise by :mod:`json`.

    Usage:

    .. code-block:: python

        try:
            json.dumps
        except ValueError as error:
            raise JSONError from error

    """


@dataclass(frozen=True, slots=True)
class DateTimeRange:
    """
    The value object represents the date and time range.
    """

    since: datetime
    till: datetime

    def __post_init__(self) -> None:
        """check the boundaries since < till"""

    @property
    def since_timestamp(self) -> int:
        return int((self.since - datetime(1970, 1, 1)).total_seconds())

    @property
    def till_timestamp(self) -> int:
        return int((self.till - datetime(1970, 1, 1)).total_seconds())

    @property
    def duration(self) -> int:
        return NotImplemented


@dataclass(frozen=True, slots=True)
class Name:
    value: str

    def __post_init__(self) -> None:
        if 0 == len(self.value):  # Yoda
            raise ValueError("Empty name is not allowed")


#                               Aggregates                                  #
# ######################################################################### #

Timestamp: TypeAlias = float
"""The (Unix) timestamp alias for primitive float value."""
# type Timestamp = float
# NOTE PEP 695 type aliases are not yet supported by Mypy (2023-01-08)


Identifier = TypeVar("Identifier", bound=Hashable)
"""The identifier is unique per aggregate. Must be immutable and hashable, e.g., 'int', 'UUID', tuple, etc.
Remember that an identifier should match domain needs; it doesn't have to always be an integer or UUID."""


class Identifiable(Protocol, Generic[Identifier]):  # type: ignore
    """
    Represents an entity with identifier.
    """

    @property
    def identifier(self) -> Identifier:
        """The entitie's unique identifier."""


class Entity(ABC, Generic[Identifier]):
    """
    An entity object in the terms of Doman-driven design.

    :param identifier:
    """

    def __init__(self, identifier: Identifier):
        self._identifier: Identifier = identifier

    @property
    def identifier(self) -> Identifier:
        return self._identifier

    def __eq__(self, other: object) -> bool:
        return isinstance(other, type(self)) and self.identifier == other.identifier

    def __hash__(self) -> int:
        return hash((type(self), self.identifier))

    def __str__(self) -> str:
        fields = inspect.getmembers(type(self), lambda a: not (inspect.isroutine(a)))
        fields_filtered = [
            f"{f[0]}={getattr(self, str(f[0]))}"
            for f in fields
            if (not f[0].startswith("_")) and (not f[0].startswith("__"))
        ]
        return f"{type(self).__name__}({','.join(fields_filtered)})"

    __repr__ = __str__  # Maybe prefer not to override this.

    # NOTE The transfer layer (data transfer object) related method.
    # Maybe use a standalone :class:`JsonEncoder` in DTO module.
    # def to_json(self): return NotImplemented


EntityType = TypeVar("EntityType", bound=Entity)

#                                Persistence                                #
# ######################################################################### #


class Repository(Protocol, Generic[EntityType, Identifier]):  # type: ignore
    """
    The aggregate root entitiy repository protocol.
    """

    def save(self, aggregate: EntityType) -> None:
        """
        Save the aggregate root entity to the storage.

        :param aggregate: The entity to save.
        """

    def find(self, aggregate_id: Identifier) -> EntityType | None:
        """
        Find the unique entity matching the predicate.

        The predicate must match exactly one or zero entity.

        :param aggregate_id: The entity to find.
        :returns: The found entity or `None`.
        """

    # def find_all(
    #     self, aggregate, predicate: Callable[[EntityType], bool]
    # ) -> Iterable[EntityType]:
    #     """Find all entities matching the predicate."""

    def exists(self, aggregate_id: Identifier) -> bool:
        """
        Check if aggregate  root entity exists in storage.

        :param aggregate_id: The entity to find.
        :returns: The `True` if found, otherwise `False`.
        """


class AbstractRepository(ABC, Generic[EntityType, Identifier]):
    """
    The aggregate root entity repository abstract class based on ODBC.

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
        aggregate_id: Identifier,
    ) -> EntityType | None:
        """
        Find a aggregate root entity matching the predicate.

        The predicate must match exactly one or zero entity.

        :param aggregate_id: The entity to find.
        :returns: The found entity or `None`.
        """

    @abstractmethod
    def exists(self, aggregate_id: Identifier) -> bool:
        """
        Check if aggregate root entity exists in the storage.

        :param aggregate_id: The entity to find.
        :returns: The `True` if found, otherwise `False`.
        """


#                                Messaging                                  #
# ######################################################################### #


@dataclass(frozen=True, slots=True)
class Event:
    pass


@dataclass(frozen=True, slots=True)
class Command:
    pass


#                                Exceptions                                 #
# ######################################################################### #


class DomainError(Exception):
    """
    Represents an exception raised in domain layer.
    """

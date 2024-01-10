"""
This module contains a shared code.
"""

# mypy: disable-error-code=empty-body
# Mypy is not smart enough to figure out that your decorator calls `abc.abstractmethod`

from abc import ABC
from typing import TypeVar, Generic, Protocol
from dataclasses import dataclass
from datetime import datetime


__all__ = ["Entity"]


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


type Timestamp = float  # type: ignore
"""The timestamp alias for primitive float value."""  # PEP 695 type aliases are not yet supported by Mypy (2023-01-08)


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
        return f"{type(self).__name__}(id={self.identifier})"

    __repr__ = __str__

    # def to_json(self): return NotImplemented
    # The transfer layer (data transfer object) related function.
    # Use a standalone :class:`JsonEncoder`.

"""
This module contains a shared code.
"""

# mypy: disable-error-code=empty-body
# Mypy is not smart enough to figure out that your decorator calls `abc.abstractmethod`

from abc import ABC
from typing import TypeVar, Generic
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
    first: str
    last: str


type Timestamp = float  # type: ignore
# PEP 695 type aliases are not yet supported by Mypy (2023-01-08)

Identifier = TypeVar("Identifier")


class Entity(ABC, Generic[Identifier]):
    """
    An entity object in the terms of Doman-driven design.

    :param id:
    :param created:
    """

    def __init__(self, id: Identifier):
        self._id = id

    @property
    def id(self) -> Identifier:
        return self._id

    def __eq__(self, other: object) -> bool:
        return isinstance(other, type(self)) and self.id == other.id

    def __hash__(self) -> int:
        return hash((type(self), self.id))

    def __str__(self) -> str:
        return f"{type(self).__name__}(id={self.id})"

    __repr__ = __str__

    # def to_json(self): return NotImplemented
    # The transfer layer (data transfer object) related function.
    # Use a standalone :class:`JsonEncoder`.

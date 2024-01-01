"""
TODO

14:15
"""

from typing import Iterable, Any, Self
import datetime
from dataclasses import dataclass
from abc import ABC


@dataclass(frozen=True, slots=True)
class DateTimeRange:
    """
    The value object represents the date and time range.
    """
    lower_bound: datetime.datetime
    upper_bound: datetime.datetime
    
    def __post_init__(self) -> None:
        """check the boundaries lower >= upper"""


@dataclass(frozen=True, slots=True)
class Name:
    first: str
    last: str


class Entity(ABC):
    def __init__(self, entity_id: int):
        self._entity_id = entity_id

    def __eq__(self, other: object) -> bool:
        return isinstance(other, type(self)) and self._entity_id == other._entity_id 

    @property
    def id(self) -> int:
        return self._entity_id        

    def hash(self) -> int:
        return hash((type(self, self._entity_id)))

    # abstractmethod?
    def to_json(self):
        # The transfer layer (data transfer object) related function.
        # Can also be a standalone :class:`JsonEncoder`.
        return NotImplemented


class User(Entity):
    """
    Represents the user domain model entity.
    """
    def __init__(self, user_id: int, name: str, city: str) -> None:
        super().__init__(entity_id=user_id)
        self._name = name
        self._city = city

    @property
    def name(self) -> str:
        return self._name
    
    def city(self) -> str:
        return self._city

    # or use setter, but I prefer immutability

    def with_changed_name(self, name: str) -> Self:
        return type(self)(user_id=self.id, name=name)
    

class Order(Entity):
    def __init__(self, order_id: int, products) -> None:
        super().__init__(entity_id=order_id)
        self.products = products # TODO

    # quantity


class OrderService:
    """TODO"""

    def __init__(self, user_repository, order_repository) -> None:
        self._user_repository = user_repository
        self._order_repository = order_repository

    @classmethod
    def store(cls, source) -> None:
        return NotImplemented

    def seach_orders(date_time_range: DateTimeRange) -> Iterable[Any]:
        return NotImplemented

    def search_users_by_ordered_products(limit) -> Iterable[User]:
        return NotImplemented
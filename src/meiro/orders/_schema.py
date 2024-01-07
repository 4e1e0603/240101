"""
This module contains database related code.
"""

from sqlalchemy import String, Integer, Float, create_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

from . import _domain

__all__ = [
    "User",
    "Product",
    "create_schema",
    "UserRepository",
    "OrderRepository",
    "ProductRepository",
]

# ######################################################################### #


class Base(DeclarativeBase):
    ...


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    city: Mapped[str] = mapped_column(String(64))

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, city={self.city!r})"


class Product(Base):
    __tablename__ = "product"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    price: Mapped[str] = mapped_column(Integer())

    def __repr__(self) -> str:
        return f"Product(id={self.id!r}, name={self.name!r}, price={self.price!r})"


class Order(Base):
    __tablename__ = "order"
    id: Mapped[int] = mapped_column(primary_key=True)
    created: Mapped[float] = mapped_column(Float)
    # user_id references
    # product_ids reference


def create_schema(memory=False):
    name = "sqlite://" if memory else "orders.db"
    engine = create_engine(name, echo=True)
    Base.metadata.create_all(engine)
    return engine


# ######################################################################### #


class UserRepository(_domain.AbstractRepository[_domain.User]):
    def __init__(self, connection) -> None:
        self.connection = connection

    def save(self, entity: _domain.User) -> None:
        return NotImplemented

    def find(self, entity: _domain.User) -> _domain.User | None:
        return NotImplemented


class OrderRepository(_domain.AbstractRepository[_domain.Order]):
    def __init__(self, connection) -> None:
        self.connection = connection

    def save(self, entity: _domain.Order) -> None:
        return NotImplemented

    def find(self, entity: _domain.Order) -> _domain.Order | None:
        return NotImplemented


class ProductRepository(_domain.AbstractRepository[_domain.Product]):
    def __init__(self, connection) -> None:
        self.connection = connection

    def save(self, entity: _domain.Product) -> None:
        return NotImplemented

    def find(self, entity: _domain.Product) -> _domain.Product | None:
        return NotImplemented

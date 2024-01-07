"""
The order service module.
"""

__all__ = ["main", "OrderService"]

# Aliases are the trick to keep linters calm about unused imports.
from ._service import main as main, OrderService as OrderService

"""Filter enum class."""
from enum import Enum


class FilterEnum(Enum):
    """Enum class with available filters."""

    NONE = None
    NAP = "transportportal"
    INVALID = "invalid"

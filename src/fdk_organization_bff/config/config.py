"""Configure fdk-organization-bff."""
from typing import Dict, Type, TypeVar


T = TypeVar("T", bound="Config")


class Config:
    """Configuration class."""

    _ROUTES = {
        "PING": "/ping",
        "READY": "/ready",
    }

    @classmethod
    def routes(cls: Type[T]) -> Dict[str, str]:
        """Return a dict with route-value for available views."""
        return cls._ROUTES

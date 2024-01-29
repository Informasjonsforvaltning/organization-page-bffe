"""Organization concepts data class."""

from dataclasses import dataclass


@dataclass
class OrganizationConcepts:
    """Data class with amount of organizations concepts."""

    totalCount: int
    newCount: int

"""Organization datasets data class."""

from dataclasses import dataclass


@dataclass
class OrganizationDataservices:
    """Data class with amount of organizations dataservices."""

    totalCount: int
    newCount: int

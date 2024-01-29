"""Organization informationmodel data class."""

from dataclasses import dataclass


@dataclass
class OrganizationInformationmodels:
    """Data class with amount of organizations informationmodels."""

    totalCount: int
    newCount: int

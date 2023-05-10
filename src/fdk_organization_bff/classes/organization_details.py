"""Organization details data class."""
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class OrganizationDetails:
    """Data class with details regarding an organization."""

    organizationId: str
    name: Optional[str]
    prefLabel: Dict
    orgPath: Optional[str]
    orgType: Optional[str]
    sectorCode: Optional[str]
    industryCode: Optional[str]
    homepage: Optional[str]
    seeAlso: Optional[str]
    numberOfEmployees: Optional[int]
    icon: str

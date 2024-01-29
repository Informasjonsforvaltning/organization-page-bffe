"""Organization catalog list data class."""

from dataclasses import dataclass
from typing import List

from fdk_organization_bff.classes.organization_catalog_summary import (
    OrganizationCatalogSummary,
)


@dataclass
class OrganizationCatalogList:
    """Data class wrapping a list of organization catalog summaries."""

    organizations: List[OrganizationCatalogSummary]

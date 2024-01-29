"""Organization category data classes."""

from dataclasses import dataclass
from typing import List

from fdk_organization_bff.classes.organization_catalog_summary import (
    OrganizationCatalogSummary,
)


@dataclass
class OrganizationCategory:
    """Data class wrapping a list of organization catalog summaries partitioned into a category."""

    category: OrganizationCatalogSummary
    organizations: List[OrganizationCatalogSummary]

    def sort_compare(self: "OrganizationCategory") -> str:
        """Get value for sorting."""
        nb = self.category.prefLabel.get("nb")
        return nb if nb else self.category.name


@dataclass
class OrganizationCategories:
    """Data class wrapping a list of organization categories."""

    categories: List[OrganizationCategory]

"""Organization datasets data class."""

from dataclasses import dataclass
from typing import Optional

from fdk_organization_bff.classes.catalog_quality_score import CatalogQualityScore


@dataclass
class OrganizationDatasets:
    """Data class with amount of and quality of an organizations datasets."""

    totalCount: int
    newCount: int
    authoritativeCount: int
    openCount: int
    quality: Optional[CatalogQualityScore]

"""Organization datasets data class."""
from dataclasses import dataclass
from typing import Optional

from fdk_organization_bff.classes.catalog_quality_rating import CatalogQualityRating


@dataclass
class OrganizationDatasets:
    """Data class with amount of and quality of an organizations datasets."""

    total: int
    new: int
    authoritative: int
    open: int
    quality: Optional[CatalogQualityRating]

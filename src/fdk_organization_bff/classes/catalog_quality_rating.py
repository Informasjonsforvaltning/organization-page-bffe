"""Catalog quality rating data class."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class CatalogQualityRating:
    """Data class with quality assessment category and associated percentage."""

    category: Optional[str]
    percentage: Optional[int]

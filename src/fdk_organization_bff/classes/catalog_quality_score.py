"""Catalog quality rating data class."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class CatalogQualityScore:
    """Data class with quality assessment score and associated percentage."""

    score: Optional[int]
    percentage: Optional[int]

"""Unit test cases for mappers."""
import pytest

from fdk_organization_bff.classes import CatalogQualityRating
from fdk_organization_bff.utils.mappers import (
    map_catalog_quality_rating,
    map_org_details,
)


@pytest.mark.unit
def test_map_catalog_quality_rating_handles_bad_data() -> None:
    """Check that map_catalog_quality_rating handles bad data."""
    rating_0 = map_catalog_quality_rating({"maxScore": "100", "category": "good"})
    rating_1 = map_catalog_quality_rating({"score": "56", "category": "good"})
    rating_2 = map_catalog_quality_rating({"score": "56", "maxScore": "100"})
    rating_3 = map_catalog_quality_rating(
        {"score": "str", "maxScore": "100", "category": "good"}
    )
    rating_4 = map_catalog_quality_rating(
        {"score": "56", "maxScore": "str", "category": "good"}
    )
    rating_5 = map_catalog_quality_rating(
        {"score": "56", "maxScore": "100", "category": "good"}
    )

    assert rating_0 is None
    assert rating_1 is None
    assert rating_2 is None
    assert rating_3 is None
    assert rating_4 is None
    assert rating_5 == CatalogQualityRating(percentage=56, category="good")


def test_map_org_details_handles_missing_data() -> None:
    """Response from map_org_details is None when data is missing."""
    details = map_org_details({}, {})

    assert details is None

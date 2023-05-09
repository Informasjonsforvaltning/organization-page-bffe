"""Unit test cases for mappers."""
import pytest

from fdk_organization_bff.classes import CatalogQualityScore
from fdk_organization_bff.utils.mappers import (
    map_catalog_quality_score,
    map_org_details,
)


@pytest.mark.unit
def test_map_catalog_quality_score_handles_bad_data() -> None:
    """Check that map_catalog_quality_score handles bad data."""
    rating_0 = map_catalog_quality_score(
        {"aggregations": [{"max_score": "100"}, {"max_score": "100"}]}
    )
    rating_1 = map_catalog_quality_score(
        {"aggregations": [{"score": "100"}, {"score": "100"}]}
    )
    rating_2 = map_catalog_quality_score({"aggregations": []})
    rating_3 = map_catalog_quality_score(
        {
            "aggregations": [
                {"score": "56", "max_score": "str"},
                {"score": "56", "max_score": "100"},
            ]
        }
    )
    rating_4 = map_catalog_quality_score(
        {
            "aggregations": [
                {"score": "str", "max_score": "100"},
                {"score": "56", "max_score": "100"},
            ]
        }
    )
    rating_5 = map_catalog_quality_score(
        {
            "aggregations": [
                {"score": "56", "max_score": "100"},
                {"score": "56", "max_score": "100"},
            ]
        }
    )

    assert rating_0 is None
    assert rating_1 is None
    assert rating_2 is None
    assert rating_3 is None
    assert rating_4 is None
    assert rating_5 == CatalogQualityScore(score=112, percentage=56)


@pytest.mark.unit
def test_map_org_details_handles_missing_data() -> None:
    """Response from map_org_details is None when data is missing."""
    details = map_org_details({}, {})

    assert details is None

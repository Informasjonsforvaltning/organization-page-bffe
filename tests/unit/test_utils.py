"""Unit test cases for utils."""
import pytest

from fdk_organization_bff.utils.utils import dataset_is_new, url_with_params


@pytest.mark.unit
def test_url_with_params() -> None:
    """Params is added correctly."""
    url_0 = url_with_params("http://localhost:8000/endpoint", None)
    url_1 = url_with_params("http://localhost:8000/endpoint", {})
    url_2 = url_with_params("http://localhost:8000/endpoint", {"key0": "value0"})
    url_3 = url_with_params(
        "http://localhost:8000/endpoint", {"key0": "value0", "key1": "value1"}
    )

    assert url_0 == "http://localhost:8000/endpoint"
    assert url_1 == "http://localhost:8000/endpoint"
    assert url_2 == "http://localhost:8000/endpoint?key0=value0"
    assert url_3 == "http://localhost:8000/endpoint?key0=value0&key1=value1"


@pytest.mark.unit
def test_dataset_is_new_handles_bad_date_format() -> None:
    """Check that dataset_is_new handles bad data."""
    res_0 = dataset_is_new({})
    res_1 = dataset_is_new({"issued": {}})
    res_2 = dataset_is_new({"issued": {"value": "2020/10/10"}})

    assert res_0 is False
    assert res_1 is False
    assert res_2 is False

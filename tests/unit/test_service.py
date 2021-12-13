"""Unit test cases for service."""
import asyncio
from typing import Any

from asynctest import CoroutineMock, MagicMock, patch
import pytest

from fdk_organization_bff.classes import FilterEnum
from fdk_organization_bff.service import org_catalog_service


def async_test(coro: Any) -> Any:
    """Async test wrapper."""

    def wrapper(*args: str, **kwargs: int) -> Any:
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(coro(*args, **kwargs))
        finally:
            loop.close()

    return wrapper


@patch("aiohttp.ClientSession.closed")
@async_test
@pytest.mark.unit
async def test_get_organization_catalog_with_closed_session(mock: MagicMock) -> None:
    """Mock closed session and get organization catalog."""
    mock.return_value.__aenter__.return_value = CoroutineMock(side_effect=True)
    org = await org_catalog_service.get_organization_catalog(
        "12345678", FilterEnum.NONE
    )
    assert org is None


@patch("aiohttp.ClientSession.closed")
@async_test
@pytest.mark.unit
async def test_get_organization_catalogs_with_closed_session(mock: MagicMock) -> None:
    """Mock closed session and get organization catalogs."""
    mock.return_value.__aenter__.return_value = CoroutineMock(side_effect=True)
    org = await org_catalog_service.get_organization_catalogs(FilterEnum.NONE)
    assert len(org.organizations) == 0

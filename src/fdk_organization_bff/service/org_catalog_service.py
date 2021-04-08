"""Service layer module for fdk-organization-bff."""
import asyncio
import logging
from typing import Dict, List, Optional, Union

from aiohttp import ClientSession

from fdk_organization_bff.classes import OrganizationCatalog
from fdk_organization_bff.config import Config
from fdk_organization_bff.sparql.queries import build_org_datasets_query
from fdk_organization_bff.utils.mappers import map_org_datasets, map_org_details
from fdk_organization_bff.utils.utils import url_with_params


async def fetch_json_data(
    url: str, params: Optional[Dict[str, str]], session: ClientSession
) -> Optional[Union[Dict, List]]:
    """Fetch json data from url."""
    async with session.get(url_with_params(url, params)) as response:
        return await response.json() if response.status == 200 else None


async def fetch_org_cat_data(id: str, session: ClientSession) -> Dict:
    """Fetch organization data from organization-catalogue."""
    url = f"{Config.org_cat_uri()}/organizations/{id}"
    org_cat_data = await fetch_json_data(url, None, session)
    if org_cat_data and isinstance(org_cat_data, Dict):
        return org_cat_data
    else:
        return dict()


async def fetch_brreg_data(id: str, session: ClientSession) -> Dict:
    """Fetch organization data from Enhetsregisteret."""
    url = f"{Config.data_brreg_uri()}/enhetsregisteret/api/enheter/{id}"
    brreg_data = await fetch_json_data(url, None, session)
    if brreg_data and isinstance(brreg_data, Dict):
        return brreg_data
    else:
        return dict()


async def query_publisher_datasets(id: str, session: ClientSession) -> Dict:
    """Query publisher datasets from fdk-sparql-service."""
    url = f"{Config.portal_uri()}/sparql"
    params = {"query": build_org_datasets_query(id)}
    datasets = await fetch_json_data(url, params, session)
    if datasets and isinstance(datasets, Dict):
        return datasets
    else:
        return dict()


async def fetch_org_datasets_assessment(id: str, session: ClientSession) -> Dict:
    """Fetch organization datasets assessment from fdk-metadata-quality-service."""
    url = f"{Config.metadata_uri()}/assessment/catalog/rating"
    params = {"entityType": "dataset", "catalogId": id}
    assessment = await fetch_json_data(url, params, session)
    if assessment and isinstance(assessment, Dict):
        return assessment
    else:
        return dict()


async def fetch_open_licenses(session: ClientSession) -> List:
    """Fetch open licenses from fdk-reference-data."""
    url = f"{Config.portal_uri()}/reference-data/codes/openlicenses"
    open_licenses = await fetch_json_data(url, None, session)
    return (
        [open_license.get("uri") for open_license in open_licenses]
        if open_licenses
        else []
    )


async def get_organization_catalog(id: str) -> Optional[OrganizationCatalog]:
    """Return specific organization catalog."""
    logging.info(f"Fetching catalog for organization with id {id}")

    async with ClientSession() as session:
        responses = await asyncio.gather(
            asyncio.ensure_future(fetch_org_cat_data(id, session)),
            asyncio.ensure_future(fetch_brreg_data(id, session)),
            asyncio.ensure_future(query_publisher_datasets(id, session)),
            asyncio.ensure_future(fetch_org_datasets_assessment(id, session)),
            asyncio.ensure_future(fetch_open_licenses(session)),
        )

    results = responses[2].get("results")
    org_datasets = results.get("bindings") if results else []

    if org_datasets and len(org_datasets) > 0:
        return OrganizationCatalog(
            organization=map_org_details(responses[0], responses[1]),
            datasets=map_org_datasets(org_datasets, responses[3], responses[4]),
        )
    else:
        return None

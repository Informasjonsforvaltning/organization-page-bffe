"""Service layer module for fdk-organization-bff."""
import asyncio
import logging
from typing import Dict, List, Optional, Union

from aiohttp import ClientSession

from fdk_organization_bff.classes import OrganizationCatalog, OrganizationCatalogList
from fdk_organization_bff.config import Config
from fdk_organization_bff.sparql.queries import (
    build_dataservices_by_publisher_query,
    build_datasets_by_publisher_query,
    build_org_datasets_query,
)
from fdk_organization_bff.utils.mappers import (
    count_list_from_sparql_response,
    expand_open_licenses_with_https,
    map_org_datasets,
    map_org_details,
    map_org_summaries,
)
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


async def fetch_all_organizations(session: ClientSession) -> Dict:
    """Fetch all organizations from organization-catalogue."""
    url = f"{Config.org_cat_uri()}/organizations"
    org_list = await fetch_json_data(url, None, session)
    return {org["organizationId"]: org for org in org_list} if org_list else dict()


async def fetch_brreg_data(id: str, session: ClientSession) -> Dict:
    """Fetch organization data from Enhetsregisteret."""
    url = f"{Config.data_brreg_uri()}/enhetsregisteret/api/enheter/{id}"
    brreg_data = await fetch_json_data(url, None, session)
    if brreg_data and isinstance(brreg_data, Dict):
        return brreg_data
    else:
        return dict()


async def query_sparql_service(query: str, session: ClientSession) -> Dict:
    """Query fdk-sparql-service."""
    url = f"{Config.portal_uri()}/sparql"
    params = {"query": query}
    datasets = await fetch_json_data(url, params, session)
    if datasets and isinstance(datasets, Dict):
        return datasets
    else:
        return dict()


async def query_publisher_datasets(id: str, session: ClientSession) -> List:
    """Query publisher datasets from fdk-sparql-service."""
    response = await query_sparql_service(build_org_datasets_query(id), session)
    results = response.get("results")
    org_datasets = results.get("bindings") if results else []
    return org_datasets if org_datasets else []


async def query_all_dataservices_ordered_by_publisher(session: ClientSession) -> List:
    """Query all dataservices from fdk-sparql-service and order by publisher."""
    response = await query_sparql_service(
        build_dataservices_by_publisher_query(), session
    )
    return count_list_from_sparql_response(response)


async def query_all_datasets_ordered_by_publisher(session: ClientSession) -> List:
    """Query all datasets from fdk-sparql-service and order by publisher."""
    response = await query_sparql_service(build_datasets_by_publisher_query(), session)
    return count_list_from_sparql_response(response)


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
    license_uris = (
        [open_license.get("uri") for open_license in open_licenses]
        if open_licenses
        else []
    )

    return expand_open_licenses_with_https(license_uris)


async def get_organization_catalog(id: str) -> Optional[OrganizationCatalog]:
    """Return specific organization catalog."""
    logging.debug(f"Fetching catalog for organization with id {id}")

    async with ClientSession() as session:
        responses = await asyncio.gather(
            asyncio.ensure_future(fetch_org_cat_data(id, session)),
            asyncio.ensure_future(fetch_brreg_data(id, session)),
            asyncio.ensure_future(query_publisher_datasets(id, session)),
            asyncio.ensure_future(fetch_org_datasets_assessment(id, session)),
            asyncio.ensure_future(fetch_open_licenses(session)),
        )

    """Respond with None if no datasets are found."""
    if responses[2] and len(responses[2]) > 0:
        return OrganizationCatalog(
            organization=map_org_details(
                org_cat_data=responses[0], brreg_data=responses[1]
            ),
            datasets=map_org_datasets(
                org_datasets=responses[2],
                assessment_data=responses[3],
                open_licenses=responses[4],
            ),
        )
    else:
        return None


async def get_organization_catalogs() -> OrganizationCatalogList:
    """Return all organization catalogs."""
    logging.debug("Fetching all catalogs")

    async with ClientSession() as session:
        responses = await asyncio.gather(
            asyncio.ensure_future(fetch_all_organizations(session)),
            asyncio.ensure_future(query_all_datasets_ordered_by_publisher(session)),
            asyncio.ensure_future(query_all_dataservices_ordered_by_publisher(session)),
        )
    return OrganizationCatalogList(
        organizations=map_org_summaries(
            organizations=responses[0], datasets=responses[1], dataservices=responses[2]
        )
    )

"""Service layer module for fdk-organization-bff."""
import asyncio
import logging
from typing import cast, Dict, List, Optional

from aiohttp import ClientSession

from fdk_organization_bff.classes import (
    FilterEnum,
    OrganizationCatalog,
    OrganizationCatalogList,
)
from fdk_organization_bff.service.adapter import (
    fetch_all_organizations,
    fetch_brreg_data,
    fetch_org_cat_data,
    fetch_org_dataset_catalog_scores,
    query_all_concepts_ordered_by_publisher,
    query_all_dataservices_ordered_by_publisher,
    query_all_datasets_ordered_by_publisher,
    query_all_informationmodels_ordered_by_publisher,
    query_publisher_concepts,
    query_publisher_dataservices,
    query_publisher_datasets,
    query_publisher_informationmodels,
)
from fdk_organization_bff.utils.mappers import (
    empty_concepts,
    empty_dataservices,
    empty_datasets,
    empty_informationmodels,
    map_org_concepts,
    map_org_dataservices,
    map_org_datasets,
    map_org_details,
    map_org_informationmodels,
    map_org_summaries,
)


async def get_organization_catalog(
    id: str, filter: FilterEnum
) -> Optional[OrganizationCatalog]:
    """Return specific organization catalog."""
    logging.debug(f"Fetching catalog for organization with id {id}")

    async with ClientSession() as session:
        (
            org_cat_data,
            brreg_data,
            org_datasets,
            org_dataservices,
            org_concepts,
            org_informationmodels,
        ) = await asyncio.gather(
            asyncio.ensure_future(fetch_org_cat_data(id, session)),
            asyncio.ensure_future(fetch_brreg_data(id, session)),
            asyncio.ensure_future(query_publisher_datasets(id, filter, session)),
            asyncio.ensure_future(query_publisher_dataservices(id, filter, session)),
            asyncio.ensure_future(query_publisher_concepts(id, filter, session)),
            asyncio.ensure_future(
                query_publisher_informationmodels(id, filter, session)
            ),
            return_exceptions=True,
        )

    if isinstance(org_cat_data, BaseException):
        logging.warning("Unable to fetch org catalog data")
        org_cat_data = None
    if isinstance(brreg_data, BaseException):
        logging.warning("Unable to fetch Brreg data")
        brreg_data = None
    if isinstance(org_datasets, BaseException):
        logging.warning("Unable to fetch org datasets")
        org_datasets = []
    if isinstance(org_dataservices, BaseException):
        logging.warning("Unable to fetch org dataservices")
        org_dataservices = []
    if isinstance(org_concepts, BaseException):
        logging.warning("Unable to fetch org concepts")
        org_concepts = []
    if isinstance(org_informationmodels, BaseException):
        logging.warning("Unable to fetch org info models")
        org_informationmodels = []

    org_datasets_scores = {}
    if len(org_datasets) > 0:
        dataset_uris = [ds["dataset"]["value"] for ds in org_datasets]
        async with ClientSession() as session:
            org_datasets_scores = await asyncio.ensure_future(
                fetch_org_dataset_catalog_scores(dataset_uris, session)
            )

    if isinstance(org_datasets_scores, BaseException):
        logging.warning("Unable to fetch org datasets scores")
        org_datasets_scores = {}

    logging.debug("Counts ")

    """Respond with None if no data is found."""
    if (
        None
        not in (org_datasets, org_dataservices, org_concepts, org_informationmodels)
        and (
            len(org_datasets)
            + len(org_dataservices)
            + len(org_concepts)
            + len(org_informationmodels)
        )
        > 0
    ):
        return OrganizationCatalog(
            organization=map_org_details(
                org_cat_data=org_cat_data, brreg_data=brreg_data
            ),
            datasets=map_org_datasets(
                org_datasets=org_datasets,
                score_data=org_datasets_scores,
            ),
            dataservices=map_org_dataservices(org_dataservices=org_dataservices),
            concepts=map_org_concepts(org_concepts=org_concepts),
            informationmodels=map_org_informationmodels(
                org_informationmodels=org_informationmodels
            ),
        )
    elif org_cat_data is not None and len(org_cat_data) > 0:
        return OrganizationCatalog(
            organization=map_org_details(
                org_cat_data=org_cat_data, brreg_data=brreg_data
            ),
            datasets=empty_datasets(),
            dataservices=empty_dataservices(),
            concepts=empty_concepts(),
            informationmodels=empty_informationmodels(),
        )
    else:
        return None


async def get_organization_catalogs(
    filter: FilterEnum, include_empty: Optional[str]
) -> OrganizationCatalogList:
    """Return all organization catalogs."""
    logging.debug("Fetching all catalogs")

    async with ClientSession() as session:
        (
            organizations,
            datasets,
            dataservices,
            concepts,
            informationmodels,
        ) = await asyncio.gather(
            asyncio.ensure_future(fetch_all_organizations(session)),
            asyncio.ensure_future(
                query_all_datasets_ordered_by_publisher(filter, session)
            ),
            asyncio.ensure_future(
                query_all_dataservices_ordered_by_publisher(filter, session)
            ),
            asyncio.ensure_future(
                query_all_concepts_ordered_by_publisher(filter, session)
            ),
            asyncio.ensure_future(
                query_all_informationmodels_ordered_by_publisher(filter, session)
            ),
            return_exceptions=True,
        )

    if isinstance(organizations, BaseException):
        logging.warning("Unable to fetch all organizations")
        organizations = {}
    if isinstance(datasets, BaseException):
        logging.warning("Unable to fetch datasets")
        datasets = []
    if isinstance(dataservices, BaseException):
        logging.warning("Unable to fetch dataservices")
        dataservices = []
    if isinstance(concepts, BaseException):
        logging.warning("Unable to fetch concepts")
        concepts = []
    if isinstance(informationmodels, BaseException):
        logging.warning("Unable to fetch informationmodels")
        informationmodels = []

    return OrganizationCatalogList(
        organizations=map_org_summaries(
            organizations=cast(Dict, organizations),
            datasets=cast(List, datasets),
            dataservices=cast(List, dataservices),
            concepts=cast(List, concepts),
            informationmodels=cast(List, informationmodels),
            include_empty=include_empty.lower() == "true" if include_empty else False,
        )
    )

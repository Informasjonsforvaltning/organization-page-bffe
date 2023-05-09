"""Service layer module for fdk-organization-bff."""
import asyncio
import logging
from typing import cast, Dict, List, Optional, Union

from aiohttp import ClientSession

from fdk_organization_bff.classes import (
    FilterEnum,
    OrganizationCatalog,
    OrganizationCatalogList,
)
from fdk_organization_bff.config import Config
from fdk_organization_bff.sparql.concept_queries import (
    build_concepts_by_publisher_query,
    build_org_concepts_query,
)
from fdk_organization_bff.sparql.dataservice_queries import (
    build_dataservices_by_publisher_query,
    build_org_dataservice_query,
)
from fdk_organization_bff.sparql.dataset_queries import (
    build_datasets_by_publisher_query,
    build_nap_datasets_by_publisher_query,
    build_nap_org_datasets_query,
    build_org_datasets_query,
)
from fdk_organization_bff.sparql.informationmodel_queries import (
    build_informationmodels_by_publisher_query,
    build_org_informationmodels_query,
)
from fdk_organization_bff.utils.mappers import (
    count_list_from_sparql_response,
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
from fdk_organization_bff.utils.utils import url_with_params


async def fetch_json_data(
    url: str, params: Optional[Dict[str, str]], session: ClientSession
) -> Optional[Union[Dict, List]]:
    """Fetch json data from url."""
    async with session.get(url_with_params(url, params)) as response:
        return await response.json() if response.status == 200 else None


async def fetch_json_data_with_post(
    url: str, data: Dict, session: ClientSession
) -> Optional[Union[Dict, List]]:
    """Fetch json data from url."""
    async with session.post(url, json=data) as response:
        return await response.json() if response.status == 200 else None


async def fetch_org_cat_data(id: str, session: ClientSession) -> Dict:
    """Fetch organization data from organization-catalog."""
    url = f"{Config.org_cat_uri()}/organizations/{id}"
    org_cat_data = await fetch_json_data(url, None, session)
    if org_cat_data and isinstance(org_cat_data, Dict):
        return org_cat_data
    else:
        return dict()


async def fetch_all_organizations(session: ClientSession) -> Dict:
    """Fetch all organizations from organization-catalog."""
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
    url = f"{Config.sparql_uri()}"
    params = {"query": query}
    datasets = await fetch_json_data(url, params, session)
    if datasets and isinstance(datasets, Dict):
        return datasets
    else:
        return dict()


async def query_publisher_datasets(
    id: str, filter: FilterEnum, session: ClientSession
) -> List:
    """Query publisher datasets from fdk-sparql-service."""
    if filter is FilterEnum.NAP:
        query = build_nap_org_datasets_query(id)
    else:
        query = build_org_datasets_query(id)

    response = await query_sparql_service(query, session)
    results = response.get("results")
    org_datasets = results.get("bindings") if results else []
    return org_datasets if org_datasets else []


async def query_publisher_informationmodels(
    id: str, filter: FilterEnum, session: ClientSession
) -> List:
    """Query publisher informationmodels from fdk-sparql-service."""
    if filter is FilterEnum.NAP:
        return list()

    results = (
        await query_sparql_service(build_org_informationmodels_query(id), session)
    ).get("results")
    org_concepts = results.get("bindings") if results else []

    return org_concepts if org_concepts else []


async def query_publisher_concepts(
    id: str, filter: FilterEnum, session: ClientSession
) -> List:
    """Query publisher concepts from fdk-sparql-service."""
    if filter is FilterEnum.NAP:
        return list()

    results = (await query_sparql_service(build_org_concepts_query(id), session)).get(
        "results"
    )
    org_concepts = results.get("bindings") if results else []

    return org_concepts if org_concepts else []


async def query_publisher_dataservices(
    id: str, filter: FilterEnum, session: ClientSession
) -> List:
    """Query publisher dataservices from fdk-sparql-service."""
    if filter is FilterEnum.NAP:
        return list()
    else:
        response = await query_sparql_service(build_org_dataservice_query(id), session)
        results = response.get("results")
        org_dataservices = results.get("bindings") if results else []
        return org_dataservices if org_dataservices else []


async def query_all_dataservices_ordered_by_publisher(
    filter: FilterEnum, session: ClientSession
) -> List:
    """Query all dataservices from fdk-sparql-service and order by publisher."""
    if filter is FilterEnum.NAP:
        return list()
    else:
        response = await query_sparql_service(
            build_dataservices_by_publisher_query(), session
        )
        return count_list_from_sparql_response(response)


async def query_all_concepts_ordered_by_publisher(
    filter: FilterEnum, session: ClientSession
) -> List:
    """Query all dataservices from fdk-sparql-service and order by publisher."""
    if filter is FilterEnum.NAP:
        return list()
    else:
        response = await query_sparql_service(
            build_concepts_by_publisher_query(), session
        )
        return count_list_from_sparql_response(response)


async def query_all_informationmodels_ordered_by_publisher(
    filter: FilterEnum, session: ClientSession
) -> List:
    """Query all dataservices from fdk-sparql-service and order by publisher."""
    if filter is FilterEnum.NAP:
        return list()
    else:
        response = await query_sparql_service(
            build_informationmodels_by_publisher_query(), session
        )
        return count_list_from_sparql_response(response)


async def query_all_datasets_ordered_by_publisher(
    filter: FilterEnum, session: ClientSession
) -> List:
    """Query all datasets from fdk-sparql-service and order by publisher."""
    if filter is FilterEnum.NAP:
        query = build_nap_datasets_by_publisher_query()
    else:
        query = build_datasets_by_publisher_query()

    response = await query_sparql_service(query, session)
    return count_list_from_sparql_response(response)


async def fetch_org_dataset_catalog_scores(
    uris: List[str], session: ClientSession
) -> Dict:
    """Fetch rating for organization's dataset catalog from fdk-metadata-quality-service."""
    url = f"{Config.metadata_uri()}/api/scores"

    scores = await fetch_json_data_with_post(url, {"datasets": uris}, session)

    if scores and isinstance(scores, Dict):
        return scores
    else:
        return dict()


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


async def get_organization_catalogs(filter: FilterEnum) -> OrganizationCatalogList:
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
        )
    )

import asyncio
import logging
import time
from typing import List, Union, Dict, Any

from src.responses import OrganizationCatalogListResponse
from src.result_readers import OrganizationStore, OrganizationReferencesObject
from src.service_requests import (
    get_organizations_from_catalog,
    get_concepts,
    get_datasets,
    get_datasets_for_transportportal,
    get_dataservices,
    get_informationmodels
)
from src.utils import FetchFromServiceException, ServiceKey


def get_organization_catalog_list() -> Union[OrganizationCatalogListResponse, Dict[str, Any]]:
    start = time.time()
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        [
            organizations,
            concepts,
            datasets,
            dataservices,
            informationmodels
        ] = loop.run_until_complete(
            asyncio.gather(
                get_organizations_from_catalog(),
                get_concepts(),
                get_datasets(),
                get_dataservices(),
                get_informationmodels()
            )
        )

        logging.debug(f"data collection took {time.time() - start}")

        return combine_results(
            organizations=OrganizationReferencesObject.from_organization_catalog_list_response(organizations),
            concepts=OrganizationReferencesObject.from_es_response_list(ServiceKey.CONCEPTS, concepts),
            informationmodels=OrganizationReferencesObject.from_es_response_list(ServiceKey.INFO_MODELS, informationmodels),
            datasets=OrganizationReferencesObject.from_sparql_bindings(ServiceKey.DATASETS, datasets),
            dataservices=OrganizationReferencesObject.from_sparql_bindings(ServiceKey.DATA_SERVICES, dataservices)

        )
    except FetchFromServiceException as err:
        return err.__dict__


def get_organization_catalog_list_for_transportportal() -> Union[OrganizationCatalogListResponse, Dict[str, Any]]:
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        [_, datasets] = loop.run_until_complete(
            asyncio.gather(
                get_organizations_from_catalog(),
                get_datasets_for_transportportal()
            )
        )

        return combine_results(
            datasets=OrganizationReferencesObject.from_sparql_bindings(ServiceKey.DATASETS, datasets)
        )
    except FetchFromServiceException as err:
        return err.__dict__


def combine_results(
        organizations: List[OrganizationReferencesObject] = None,
        concepts: List[OrganizationReferencesObject] = None,
        datasets: List[OrganizationReferencesObject] = None,
        dataservices: List[OrganizationReferencesObject] = None,
        informationmodels: List[OrganizationReferencesObject] = None
) -> OrganizationCatalogListResponse:
    loop = asyncio.get_event_loop()
    store = OrganizationStore.get_instance()

    if not store.clear_content_count():
        loop.run_until_complete(store.add_all(
            organizations=organizations or [],
            for_service=ServiceKey.ORGANIZATIONS)
        )

    loop.run_until_complete(asyncio.gather(
        store.add_all(
            organizations=informationmodels or [],
            for_service=ServiceKey.INFO_MODELS
        ),
        store.add_all(
            organizations=concepts or [],
            for_service=ServiceKey.CONCEPTS
        ),
        store.add_all(
            organizations=datasets or [],
            for_service=ServiceKey.DATASETS
        ),
        store.add_all(
            organizations=dataservices or [],
            for_service=ServiceKey.DATA_SERVICES)
    ))

    return OrganizationCatalogListResponse.from_organization_store(store)

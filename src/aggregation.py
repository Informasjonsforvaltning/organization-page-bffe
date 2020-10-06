import asyncio
import logging
import time
import re
from typing import List

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


def get_organization_catalog_list() -> OrganizationCatalogListResponse:
    start = time.time()
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        content_requests = asyncio.gather(get_organizations_from_catalog(),
                                          get_concepts(),
                                          get_datasets(),
                                          get_dataservices(),
                                          get_informationmodels())
        organizations, concepts, datasets, dataservices, informationmodels = loop.run_until_complete(content_requests)
        logging.debug(f"data collection took {time.time() - start}")

        return combine_results(
            organizations=OrganizationReferencesObject.from_organization_catalog_list_response(organizations),
            concepts=OrganizationReferencesObject.from_es_response_list(for_service=ServiceKey.CONCEPTS,
                                                                        es_response=concepts),
            informationmodels=OrganizationReferencesObject.from_es_response_list(for_service=ServiceKey.INFO_MODELS,
                                                                                 es_response=informationmodels),
            datasets=OrganizationReferencesObject.from_sparql_bindings(for_service=ServiceKey.DATASETS,
                                                                       sparql_bindings=datasets),
            dataservices=OrganizationReferencesObject.from_sparql_bindings(for_service=ServiceKey.DATA_SERVICES,
                                                                           sparql_bindings=dataservices)

        )
    except FetchFromServiceException as err:
        return err.__dict__


def get_organization_catalog_list_for_transportportal() -> OrganizationCatalogListResponse:
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        organizations, datasets = loop.run_until_complete(
            asyncio.gather(
                get_organizations_from_catalog(),
                get_datasets_for_transportportal()
            )
        )

        norwegian_registry_pattern = re.compile(r"^https://data.brreg.no/enhetsregisteret/api/enheter/\d{9}$")

        transportportal_norwegian_registry_ids = list(filter(
            lambda norwegian_registry_id: re.search(norwegian_registry_pattern, norwegian_registry_id),
            map(lambda dataset: dataset["publisher"]["value"], datasets)
        ))

        transportportal_organizations = filter(lambda o: o["norwegianRegistry"] in transportportal_norwegian_registry_ids, organizations)
        transportportal_datasets = filter(lambda d: d["publisher"]["value"] in transportportal_norwegian_registry_ids, datasets)

        return combine_results(
            organizations=OrganizationReferencesObject.from_organization_catalog_list_response(transportportal_organizations),
            datasets=OrganizationReferencesObject.from_sparql_bindings(ServiceKey.DATASETS, transportportal_datasets),
            concepts=[],
            informationmodels=[],
            dataservices=[]
        )
    except FetchFromServiceException as err:
        return err.__dict__


def combine_results(organizations: List[OrganizationReferencesObject],
                    concepts: List[OrganizationReferencesObject],
                    datasets: List[OrganizationReferencesObject],
                    dataservices: List[OrganizationReferencesObject],
                    informationmodels: List[OrganizationReferencesObject]) -> OrganizationCatalogListResponse:
    loop = asyncio.get_event_loop()
    store = OrganizationStore.get_instance()

    if not store.clear_content_count():
        loop.run_until_complete(store.add_all(organizations=organizations,
                                              for_service=ServiceKey.ORGANIZATIONS))
    add_tasks = asyncio.gather(
        store.add_all(organizations=informationmodels,
                      for_service=ServiceKey.INFO_MODELS
                      ),
        store.add_all(organizations=concepts,
                      for_service=ServiceKey.CONCEPTS),
        store.add_all(organizations=datasets,
                      for_service=ServiceKey.DATASETS),
        store.add_all(organizations=dataservices,
                      for_service=ServiceKey.DATA_SERVICES))
    loop.run_until_complete(add_tasks)
    return OrganizationCatalogListResponse.from_organization_store(store)

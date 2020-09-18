import asyncio
import logging
import time
from typing import List

from src.responses import OrganizationCatalogListResponse
from src.result_readers import OrganizationStore, OrganizationReferencesObject
from src.service_requests import get_organizations_from_catalog, get_concepts, get_datasets, get_dataservices, \
    get_informationmodels
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
            dataservices=OrganizationReferencesObject.from_sparql_bindings(for_service=dataservices,
                                                                           sparql_bindings=dataservices)

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

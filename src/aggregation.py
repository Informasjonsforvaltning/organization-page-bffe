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

        return combine_results(organizations, concepts, datasets, dataservices, informationmodels)
    except FetchFromServiceException as err:
        return err.__dict__


def combine_results(organizations_from_service: List[OrganizationReferencesObject],
                    concepts: List[OrganizationReferencesObject],
                    datasets: List[OrganizationReferencesObject],
                    dataservices: List[OrganizationReferencesObject],
                    informationmodels: List[OrganizationReferencesObject]) -> OrganizationCatalogListResponse:
    store = OrganizationStore.get_instance()
    store.add_all(organizations=organizations_from_service,
                  for_service=ServiceKey.ORGANIZATIONS)
    store.add_all(organizations=informationmodels,
                  for_service=ServiceKey.INFO_MODELS
                  )
    store.add_all(organizations=concepts,
                  for_service=ServiceKey.CONCEPTS)
    store.add_all(organizations=datasets,
                  for_service=ServiceKey.DATASETS)
    store.add_all(organizations=dataservices,
                  for_service=ServiceKey.DATA_SERVICES)

    return OrganizationCatalogListResponse.from_organization_store(store)

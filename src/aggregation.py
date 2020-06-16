import asyncio
import logging
import time
from asyncio import get_event_loop

from src.responses import OrganizationCatalogResponse, OrganizationCatalogListResponse
from src.service_requests import get_organizations, get_concepts, get_datasets, get_dataservices, \
    get_informationmodels, get_organization
from src.utils import FetchFromServiceException, aggregation_cache


def get_organization_catalog_list():
    start = time.time()
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        content_requests = asyncio.gather(get_organizations(),
                                          get_concepts(),
                                          get_datasets(),
                                          get_dataservices(),
                                          get_informationmodels())
        organizations, concepts, datasets, dataservices, informationmodels = loop.run_until_complete(content_requests)
        logging.debug(f"data collection took {time.time() - start}")

        return aggregate_results(organizations, concepts, datasets, dataservices, informationmodels)
    except FetchFromServiceException as err:
        return err.__dict__


@aggregation_cache
def aggregate_results(organizations_from_service, concepts, datasets, dataservices,
                      informationmodels) -> OrganizationCatalogListResponse:
    iterator = ResultIterator(organizations=organizations_from_service,
                              concepts=concepts,
                              datasets=datasets,
                              dataservices=dataservices,
                              informationmodels=informationmodels)

    response_list = OrganizationCatalogListResponse()

    while True:
        org_catalog = iterator.__next__()
        if org_catalog:
            response_list.add_organization_catalog(org_catalog)
        else:
            break

    return response_list


class ResultIterator:
    def __init__(self, organizations: list, concepts: list, datasets: list, dataservices: list,
                 informationmodels: list):
        self.organizations = organizations
        self.concepts = concepts
        self.datasets = datasets
        self.dataservices = dataservices
        self.informationmodels = informationmodels

    def __next__(self):
        if self.organizations.__len__() == 0:
            if self.__completed():
                return False
            else:
                self.__get_remaining_organizations()

        org = self.organizations.pop(0)
        return OrganizationCatalogResponse(
            organization=org,
            concepts=self.__get_concepts(org),
            dataservices=self.__get_dataservices(org),
            datasets=self.__get_datasets(org),
            informationmodels=self.__get_informationmodel(org)
        )

    def __completed(self):
        return self.informationmodels.__len__() == 0 and \
               self.datasets.__len__() == 0 and \
               self.dataservices.__len__() == 0 and \
               self.concepts.__len__() == 0

    def __get_concepts(self, org: dict):
        try:
            org_concepts_index = self.concepts.index(self.__get_organization_identifier(org))
            return self.concepts.pop(org_concepts_index)
        except ValueError:
            return None

    def __get_informationmodel(self, org: dict):
        try:
            org_info_index = self.informationmodels.index(self.__get_organization_identifier(org))
            return self.informationmodels.pop(org_info_index)
        except ValueError:
            return None

    def __get_datasets(self, org: dict):
        try:
            org_set_index = self.datasets.index(self.__get_organization_identifier(org))
            return self.datasets.pop(org_set_index)
        except ValueError:
            return None

    def __get_dataservices(self, org: dict):
        try:
            org_set_index = self.dataservices.index(self.__get_organization_identifier(org))
            return self.dataservices.pop(org_set_index)
        except ValueError:
            return None

    def __get_remaining_organizations(self):
        reduced_org_content = [org for org in set(self.datasets).union(set(self.concepts)).union(
            set(self.informationmodels).union(self.dataservices))]
        loop = get_event_loop()
        organization_tasks = asyncio.gather(*(get_organization(org) for org in reduced_org_content))
        result = loop.run_until_complete(organization_tasks)
        self.organizations.extend(result)

    @staticmethod
    def __get_organization_identifier(org: dict):
        keys = org.keys()
        if "norwegianRegistry" in keys:
            return org["norwegianRegistry"]
        elif "organizationId" in keys:
            return org["organizationId"]
        else:
            return org["name"]

from json.decoder import JSONDecodeError
import logging
import httpx
from httpcore import ConnectError, ConnectTimeout
from httpx import HTTPError, AsyncClient

from src.result_readers import read_sparql_result, parse_es_results, OrganizationReferencesObject
from src.sparql.queries import build_publisher_query
from src.utils import ServiceKey, FetchFromServiceException, encode_for_sparql, \
    get_service_url, NotInNationalRegistryException

ORGANIZATION_CATALOG_URL = get_service_url(ServiceKey.ORGANIZATIONS)
DATASET_HARVESTER_URL = get_service_url(ServiceKey.DATA_SETS)
DATASERVICE_HARVESTER_URL = get_service_url(ServiceKey.DATA_SERVICES)
CONCEPT_HARVESTER_URL = get_service_url(ServiceKey.CONCEPTS)
INFORMATION_MODEL_HARVESTER_URL = get_service_url(ServiceKey.INFO_MODELS)

default_headers = {
    'accept': 'application/json'
}


def error_msg(reason: str, serviceKey: ServiceKey):
    return {
        "status": "error",
        "service": serviceKey,
        "reason": f"{reason}"
    }


def service_error_msg(serviceKey: ServiceKey, url: str):
    return {
        "service": serviceKey,
        "reason": f"Connection error on {url}"
    }


async def get_organizations_from_catalog():
    async with httpx.AsyncClient() as client:
        try:
            result = await client.get(url=ORGANIZATION_CATALOG_URL,
                                      headers={"Accept": "application/json"},
                                      timeout=5)
            return result.json()
        except (ConnectError, HTTPError, ConnectTimeout):
            raise FetchFromServiceException(
                execution_point=ServiceKey.ORGANIZATIONS,
                url=ORGANIZATION_CATALOG_URL
            )


async def fetch_organization_from_catalog(org: OrganizationReferencesObject) -> dict:
    national_reg_id = OrganizationReferencesObject.resolve_id(org.org_uri)
    url: str = f'{ORGANIZATION_CATALOG_URL}/{national_reg_id}'
    async with AsyncClient() as session:
        try:
            response = await session.get(url=url, headers=default_headers, timeout=5)
            response.raise_for_status()

            return response.json()
        except (ConnectError, ConnectTimeout):
            raise FetchFromServiceException(
                execution_point="get organization by id",
                url=url
            )
        except (ConnectTimeout, ConnectError):
            raise FetchFromServiceException(
                execution_point="connection error to organization catalog",
                url=url
            )
        except HTTPError as err:
            if err.response.status_code == 404:
                return await attempt_fetch_organization_by_name_from_catalog(org.name)
            else:
                raise FetchFromServiceException(
                    execution_point=f"{err.response.status_code}: get organization",
                    url=url
                )


async def attempt_fetch_organization_by_name_from_catalog(name: str) -> dict:
    if name is None:
        raise NotInNationalRegistryException("No name")
    url: str = f'{ORGANIZATION_CATALOG_URL}/organizations?name={name.upper()}'
    async with AsyncClient() as session:
        try:
            response = await session.get(url=url, headers=default_headers, timeout=5)
            response.raise_for_status()
            return response.json()[0]
        except (ConnectError, ConnectTimeout):
            raise FetchFromServiceException(
                execution_point="get organization by name",
                url=url
            )
        except HTTPError as err:
            if err.response.status_code == 404:
                raise NotInNationalRegistryException(name)
            else:
                raise FetchFromServiceException(
                    execution_point=f"{err.response.status_code}: get organization",
                    url=url
                )
        except IndexError:
            raise NotInNationalRegistryException(name)


async def fetch_generated_org_path_from_organization_catalog(name: str):
    if name is None:
        return None
    url: str = f'{ORGANIZATION_CATALOG_URL}/organizations/orgpath/{name.upper()}'
    async with AsyncClient() as session:
        try:
            response = await session.get(url=url, timeout=5)
            response.raise_for_status()
            return response.text
        except (ConnectError, ConnectTimeout):
            raise FetchFromServiceException(
                execution_point="get organization by name",
                url=url
            )
        except HTTPError as err:
            raise FetchFromServiceException(
                execution_point=f"{err.response.status_code}: get organization",
                url=url
            )


async def get_concepts():
    async with httpx.AsyncClient() as client:
        try:
            es_result_list = []
            i = 0
            while True:
                result = await client.get(url=CONCEPT_HARVESTER_URL,
                                          params={"returnfields": "publisher", "size": "1000", "page": i},
                                          timeout=5)
                result.raise_for_status()
                es_result_list.extend(result.json()["_embedded"]["concepts"])
                if es_result_list.__len__() >= result.json()["page"]["totalElements"]:
                    break
                else:
                    i += 1
            return parse_es_results(es_result_list, with_uri=True)
        except (ConnectError, HTTPError, ConnectTimeout):
            raise FetchFromServiceException(
                execution_point=ServiceKey.CONCEPTS,
                url=CONCEPT_HARVESTER_URL
            )
        except JSONDecodeError:
            return {
                "page": {
                    "totalElements": 0
                }
            }


async def get_datasets():
    async with httpx.AsyncClient() as client:
        try:
            sparql_select_endpoint = f"{DATASET_HARVESTER_URL}/sparql/select"
            encoded_query = encode_for_sparql(build_publisher_query())
            print(encoded_query)
            url_with_query = f"{sparql_select_endpoint}?query={encoded_query}"
            result = await client.get(url=url_with_query, timeout=5)
            result.raise_for_status()
            return read_sparql_result(result.text)
        except (ConnectError, HTTPError, ConnectTimeout):
            logging.error("[datasets]: Error when attempting to execute SPARQL select query", )
            raise FetchFromServiceException(
                execution_point=ServiceKey.DATA_SETS,
                url=sparql_select_endpoint
            )


async def get_dataservices():
    async with httpx.AsyncClient() as client:
        try:
            sparql_select_endpoint = f"{DATASERVICE_HARVESTER_URL}/sparql/select"
            encoded_query = encode_for_sparql(build_publisher_query())
            print(encoded_query)
            url_with_query = f"{sparql_select_endpoint}?query={encoded_query}"
            result = await client.get(url=url_with_query, timeout=5)
            result.raise_for_status()
            return read_sparql_result(result.text)
        except (ConnectError, HTTPError, ConnectTimeout):
            logging.error("[dataservices]: Error when attempting to execute SPARQL select query", )
            raise FetchFromServiceException(
                execution_point=ServiceKey.DATA_SERVICES,
                url=sparql_select_endpoint
            )


async def get_informationmodels():
    async with httpx.AsyncClient() as client:
        try:
            es_result_list = []
            while True:
                result = await client.get(url=f"{INFORMATION_MODEL_HARVESTER_URL}",
                                          params={"returnfields": "publisher", "size": "10000", "page": 0},
                                          timeout=5)
                result.raise_for_status()
                es_result_list.extend(result.json()["_embedded"]["informationmodels"])
                if es_result_list.__len__() >= result.json()["page"]["totalElements"]:
                    break

            return parse_es_results(es_result_list, with_uri=True)
        except (ConnectError, HTTPError, ConnectTimeout):
            raise FetchFromServiceException(
                execution_point=ServiceKey.INFO_MODELS,
                url=INFORMATION_MODEL_HARVESTER_URL
            )
        except JSONDecodeError:
            return []

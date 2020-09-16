from json.decoder import JSONDecodeError
from os import environ as env
import logging
from typing import List

import httpx
from httpcore import ConnectError, ConnectTimeout
from httpx import HTTPError, AsyncClient

from src.result_readers import OrganizationReferencesObject
from src.sparql.queries import build_dataset_publisher_query, build_dataservices_publisher_query
from src.utils import ServiceKey, FetchFromServiceException, encode_for_sparql, \
    get_service_url, NotInNationalRegistryException, ContentKeys

ORGANIZATION_CATALOG_URL = get_service_url(ServiceKey.ORGANIZATIONS)
DATASET_HARVESTER_URL = get_service_url(ServiceKey.DATASETS)
DATASERVICE_HARVESTER_URL = get_service_url(ServiceKey.DATA_SERVICES)
CONCEPT_HARVESTER_URL = get_service_url(ServiceKey.CONCEPTS)
INFORMATION_MODEL_HARVESTER_URL = get_service_url(ServiceKey.INFO_MODELS)

default_headers = {
    'accept': 'application/json'
}

SEARCH_FULLTEXT_HOST = env.get("SEARCH_FULLTEXT_HOST")
METADATA_QUALITY_ASSESSMENT_SERVICE_HOST = env.get("METADATA_QUALITY_ASSESSMENT_SERVICE_HOST")


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


async def get_organizations_from_catalog() -> List[OrganizationReferencesObject]:
    async with httpx.AsyncClient() as client:
        try:
            result = await client.get(url=ORGANIZATION_CATALOG_URL,
                                      headers={"Accept": "application/json"},
                                      timeout=5)
            return OrganizationReferencesObject.from_organization_catalog_list_response(result.json())
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


async def fetch_generated_org_path_from_organization_catalog(name: str) -> str:
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


async def get_concepts() -> List[OrganizationReferencesObject]:
    async with httpx.AsyncClient() as client:
        try:
            result = await client.get(url=CONCEPT_HARVESTER_URL,
                                      params={"aggregations": ContentKeys.ORG_PATH, "size": "0"},
                                      timeout=5)
            result.raise_for_status()
            aggregations = result.json()[ContentKeys.AGGREGATIONS]
            return [OrganizationReferencesObject.from_es_response(es_response=bucket, for_service=ServiceKey.CONCEPTS)
                    for bucket in aggregations[ContentKeys.ORG_PATH][ContentKeys.BUCKETS]]

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


async def get_datasets() -> List[OrganizationReferencesObject]:
    async with httpx.AsyncClient() as client:
        try:
            sparql_select_endpoint = f"{DATASET_HARVESTER_URL}/sparql/select"
            encoded_query = encode_for_sparql(build_dataset_publisher_query())
            url_with_query = f"{sparql_select_endpoint}?query={encoded_query}"
            result = await client.get(url=url_with_query, timeout=5, headers=default_headers)
            result.raise_for_status()
            sparql_bindings = result.json()[ContentKeys.SPARQL_RESULTS][ContentKeys.SPARQL_BINDINGS]
            return [OrganizationReferencesObject.from_sparql_query_result(
                for_service=ServiceKey.DATASETS,
                organization=binding
            ) for binding in sparql_bindings]
        except (ConnectError, HTTPError, ConnectTimeout):
            logging.error("[datasets]: Error when attempting to execute SPARQL select query", )
            raise FetchFromServiceException(
                execution_point=ServiceKey.DATASETS,
                url=sparql_select_endpoint
            )


async def get_dataservices() -> List[OrganizationReferencesObject]:
    async with httpx.AsyncClient() as client:
        try:
            sparql_select_endpoint = f"{DATASERVICE_HARVESTER_URL}/sparql/select"
            encoded_query = encode_for_sparql(build_dataservices_publisher_query())
            url_with_query = f"{sparql_select_endpoint}?query={encoded_query}"
            result = await client.get(url=url_with_query, headers=default_headers, timeout=5)
            result.raise_for_status()
            sparql_bindings = result.json()[ContentKeys.SPARQL_RESULTS][ContentKeys.SPARQL_BINDINGS]
            return [OrganizationReferencesObject.from_sparql_query_result(
                for_service=ServiceKey.DATA_SERVICES,
                organization=binding
            ) for binding in sparql_bindings]
        except (ConnectError, HTTPError, ConnectTimeout):
            logging.error("[dataservices]: Error when attempting to execute SPARQL select query", )
            raise FetchFromServiceException(
                execution_point=ServiceKey.DATA_SERVICES,
                url=sparql_select_endpoint
            )


async def get_informationmodels():
    async with httpx.AsyncClient() as client:
        try:
            result = await client.get(url=f"{INFORMATION_MODEL_HARVESTER_URL}",
                                      params={"aggregations": "orgPath", "size": 0},
                                      timeout=5)
            result.raise_for_status()
            aggregations = result.json()[ContentKeys.AGGREGATIONS]
            return [OrganizationReferencesObject.from_es_response(es_response=bucket,
                                                                  for_service=ServiceKey.INFO_MODELS)
                    for bucket in aggregations[ContentKeys.ORG_PATH][ContentKeys.BUCKETS]]
        except (ConnectError, HTTPError, ConnectTimeout):
            raise FetchFromServiceException(
                execution_point=ServiceKey.INFO_MODELS,
                url=INFORMATION_MODEL_HARVESTER_URL
            )
        except JSONDecodeError:
            return []


async def get_organization_from_organization_catalogue(organization_id: str) -> dict:
    catalog_url = f"{ORGANIZATION_CATALOG_URL}/{organization_id}"
    async with httpx.AsyncClient() as client:
        try:
            organization = await client.get(url=catalog_url,
                                            headers={"Accept": "application/json"},
                                            timeout=1)
            organization.raise_for_status()
            return organization.json()
        except HTTPError as err:
            raise FetchFromServiceException(execution_point=ServiceKey.ORGANIZATIONS,
                                            url=catalog_url)
        except JSONDecodeError:
            raise FetchFromServiceException(execution_point=ServiceKey.ORGANIZATIONS,
                                            url=catalog_url)
        except ConnectError:
            raise FetchFromServiceException(execution_point=ServiceKey.ORGANIZATIONS,
                                            url=catalog_url)


async def search_datasets(data):
    async with httpx.AsyncClient() as client:
        url = f"{SEARCH_FULLTEXT_HOST}/datasets"

        try:
            result = await client.post(
                url=url,
                json=data,
                timeout=5
            )
            result.raise_for_status()

            return result.json()
        except (ConnectError, HTTPError, ConnectTimeout):
            logging.error("[datasets]: search request failed")
            raise FetchFromServiceException(execution_point=ServiceKey.DATASETS, url=url)


async def get_assessments_for_entities(entity_uris: List[str]):
    async with httpx.AsyncClient() as client:
        url = f"{METADATA_QUALITY_ASSESSMENT_SERVICE_HOST}/assessment/entities"
        params = {
            "entityUris": entity_uris
        }

        try:
            result = await client.get(
                url=url,
                params=params,
                timeout=5
            )
            result.raise_for_status()

            return result.json()
        except (ConnectError, HTTPError, ConnectTimeout):
            logging.error("[assessments]: assessments for entities request failed")
            raise FetchFromServiceException(execution_point=ServiceKey.DATASETS, url=url)


async def get_assessment_for_entity(entity_uri: str):
    async with httpx.AsyncClient() as client:
        url = f"{METADATA_QUALITY_ASSESSMENT_SERVICE_HOST}/assessment/entity"
        params = {
            "entityUri": entity_uri
        }

        try:
            result = await client.get(
                url=url,
                params=params,
                timeout=5
            )
            result.raise_for_status()

            return result.json()
        except (ConnectError, HTTPError, ConnectTimeout):
            logging.error("[assessments]: assessment for entity request failed")
            raise FetchFromServiceException(execution_point=ServiceKey.DATASETS, url=url)


async def get_catalog_assessment_rating_for_entity_type(catalog_uri: str, entity_type: str):
    async with httpx.AsyncClient() as client:
        url = f"{METADATA_QUALITY_ASSESSMENT_SERVICE_HOST}/assessment/catalog/rating"
        params = {
            "catalogUri": catalog_uri,
            "entityType": entity_type
        }

        try:
            result = await client.get(
                url=url,
                params=params,
                timeout=5
            )
            result.raise_for_status()

            return result.json()
        except (ConnectError, HTTPError, ConnectTimeout):
            logging.error("[assessments]: catalog assessment rating for entity type request failed")
            raise FetchFromServiceException(execution_point=ServiceKey.DATASETS, url=url)

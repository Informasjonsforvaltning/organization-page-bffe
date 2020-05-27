import os
import requests
import logging

from src.utils import ServiceKey, FetchFromServiceException


def error_msg(reason: str):
    return {
        "status": "error",
        "reason": f"{reason}"
    }


service_urls = {
    ServiceKey.ORGANIZATIONS: os.getenv('ORGANIZATION_CATALOG_URL') or "http://localhost:8080/organizations",
    ServiceKey.INFO_MODELS: os.getenv('INFORMATIONMODELS_HARVESTER_URL') or "http://localhost:8080/informationmodels",
    ServiceKey.DATA_SERVICES: os.getenv('DATASERVICE_HARVESTER_URL') or "http://localhost:8080/apis",
    ServiceKey.DATA_SETS: os.getenv('DATASET_HARVESTER_URL') or "http://localhost:8080/datasets",
    ServiceKey.CONCEPTS: os.getenv('CONCEPT_HARVESTER_URL') or "http://localhost:8080/concepts"

}


def check_available(service: ServiceKey, header=None):
    try:
        if header:
            result = requests.get(url=service_urls[service], headers=header, timeout=10)
        else:
            result = requests.get(url=service_urls[service], timeout=10)
        result.raise_for_status()
        return True
    except (requests.HTTPError, requests.RequestException, requests.Timeout) as err:
        logging.error(f"error when attempting to contact {service} on {service_urls[service]}")
        print(f"error when attempting to contact {service} on {service_urls[service]}")
        return False


def is_ready():
    logging.info("attempting to contact services")
    print("attempting to contact services")
    if not check_available(ServiceKey.ORGANIZATIONS, header={"Accept": "application/json"}):
        return error_msg(
            f" error when contacting {ServiceKey.ORGANIZATIONS} at {service_urls[ServiceKey.ORGANIZATIONS]}")
    if not check_available(ServiceKey.INFO_MODELS):
        return error_msg(f" error when contacting {ServiceKey.INFO_MODELS} at {service_urls[ServiceKey.INFO_MODELS]}")
    if not check_available(ServiceKey.DATA_SERVICES):
        return error_msg(
            f" error when contacting {ServiceKey.DATA_SERVICES} at {service_urls[ServiceKey.DATA_SERVICES]}")
    if not check_available(ServiceKey.DATA_SETS):
        return error_msg(f" error when contacting {ServiceKey.DATA_SETS} at {service_urls[ServiceKey.DATA_SETS]}")
    if not check_available(ServiceKey.CONCEPTS):
        return error_msg(f" error when contacting {ServiceKey.CONCEPTS} at {service_urls[ServiceKey.CONCEPTS]}")

    return {"status": "OK"}


def get_organizations():
    try:
        result = requests.get(url=service_urls[ServiceKey.ORGANIZATIONS],
                              headers={"Accept": "application/json"},
                              timeout=10)
        result.raise_for_status()
        return result.json()
    except (requests.HTTPError, requests.RequestException, requests.Timeout) as err:
        raise FetchFromServiceException(
            execution_point=ServiceKey.ORGANIZATIONS,
            url=service_urls[ServiceKey.ORGANIZATIONS]
        )


def get_concepts_for_organization(orgPath):
    try:
        result = requests.get(url=f"{service_urls[ServiceKey.CONCEPTS]}?orgPath={orgPath}",
                              timeout=10)
        result.raise_for_status()
        return result.json()
    except (requests.HTTPError, requests.RequestException, requests.Timeout) as err:
        raise FetchFromServiceException(
            execution_point=ServiceKey.CONCEPTS,
            url=service_urls[ServiceKey.CONCEPTS]
        )


def get_datasets_for_organization(orgPath):
    try:
        result = requests.get(url=f"{service_urls[ServiceKey.DATA_SETS]}?orgPath={orgPath}",
                              headers={"Accept": "application/json"},
                              timeout=10)
        result.raise_for_status()
        return result.json()
    except (requests.HTTPError, requests.RequestException, requests.Timeout) as err:
        raise FetchFromServiceException(
            execution_point=ServiceKey.DATA_SETS,
            url=service_urls[ServiceKey.DATA_SETS]
        )


def get_dataservices_for_organization(orgPath):
    try:
        result = requests.get(url=f"{service_urls[ServiceKey.DATA_SERVICES]}?orgPath={orgPath}",
                              timeout=10)
        result.raise_for_status()
        return result.json()
    except (requests.HTTPError, requests.RequestException, requests.Timeout) as err:
        raise FetchFromServiceException(
            execution_point=ServiceKey.DATA_SERVICES,
            url=service_urls[ServiceKey.DATA_SERVICES]
        )


def get_informationmodels_for_organization(orgPath):
    try:
        result = requests.get(url=f"{service_urls[ServiceKey.INFO_MODELS]}?orgPath={orgPath}",
                              timeout=10)
        result.raise_for_status()
        if result.json()["page"]["totalElements"] == 0:
            result = requests.get(url=f"{service_urls[ServiceKey.INFO_MODELS]}?orgPath=/{orgPath}",
                                  timeout=10)
            result.raise_for_status()
        return result.json()
    except (requests.HTTPError, requests.RequestException, requests.Timeout) as err:
        raise FetchFromServiceException(
            execution_point=ServiceKey.INFO_MODELS,
            url=service_urls[ServiceKey.INFO_MODELS]
        )


def get_org_path_for_old_harvester(orgPath: str):
    if orgPath.startswith("/"):
        return orgPath
    else:
        return f"/{orgPath}"

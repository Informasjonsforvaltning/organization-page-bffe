import os

import requests


class ServiceKey:
    ORGANIZATIONS = "organization"
    INFO_MODELS = "informationmodels"
    DATA_SERVICES = "dataservices"
    DATA_SETS = "datasets"
    CONCEPTS = "concepts"


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


def check_available(service: ServiceKey):
    try:
        result = requests.get(url=service_urls[service], timeout=10)
        result.raise_for_status()
        return True
    except (requests.HTTPError, requests.RequestException, requests.Timeout) as err:
        return False


def is_ready():
    if not check_available(ServiceKey.ORGANIZATIONS):
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

import os


class OrgCatalogKeys:
    ID = "organizationId"
    NAME = "name"
    URI = "norwegianRegistry"
    ORG_PATH = "orgPath"


class ServiceKey:
    FDK_BASE = "fdk_base"
    ORGANIZATIONS = "organizations"
    INFO_MODELS = "informationmodels"
    DATA_SERVICES = "dataservices"
    OLD_DATA_SERVICES = "apis"
    DATASETS = "datasets"
    CONCEPTS = "concepts"
    METADATA = "metadata"


class FetchFromServiceException(Exception):
    def __init__(self, execution_point: ServiceKey, url: str = None, additional_info: str = None):
        self.status = "error"
        self.reason = f"Connection error when attempting to fetch {execution_point} from {url}"
        if additional_info:
            self.reason += additional_info


env_variables = {
    ServiceKey.ORGANIZATIONS: 'ORGANIZATION_CATALOG_URL',
    ServiceKey.INFO_MODELS: 'INFORMATIONMODELS_HARVESTER_URL',
    ServiceKey.DATA_SERVICES: 'DATASERVICE_HARVESTER_URL',
    ServiceKey.DATASETS: 'DATASET_HARVESTER_URL',
    ServiceKey.CONCEPTS: 'CONCEPT_HARVESTER_URL',
    ServiceKey.FDK_BASE: 'FDK_BASE'
}


def get_service_url(service: ServiceKey):
    base_url = os.getenv(env_variables[service]) or "http://localhost:8080"
    if service == ServiceKey.DATASETS or service == ServiceKey.DATA_SERVICES or service == ServiceKey.FDK_BASE:
        return base_url
    else:
        return f"{base_url}/{service}"


class ContentKeys:
    SPARQL_RESULTS = "results"
    SPARQL_BINDINGS = "bindings"
    BUCKETS = "buckets"
    AGGREGATIONS = "aggregations"
    ORG_PATH = "orgPath"
    KEY = "key"
    SAME_AS = "sameAs"
    PUBLISHER = "publisher"
    ORGANIZATION_NUMBER = "organizationNumber"
    COUNT = "count"
    VALUE = "value"
    ORG_NAME = "name"


class NotInNationalRegistryException(Exception):
    def __init__(self, uri=None, orgs=None):
        self.reason = f"{uri} was not found in the nationalRegistry"
        self.organization = orgs


class OrganizationCatalogResult:
    def __init__(self, org_path, org_id=None, name=None):
        self.org_id = org_id
        self.name = name
        self.org_path = org_path

    @staticmethod
    def from_json(response: dict):
        return OrganizationCatalogResult(
            org_id=response[OrgCatalogKeys.ID],
            name=response[OrgCatalogKeys.NAME],
            org_path=response[OrgCatalogKeys.ORG_PATH]
        )

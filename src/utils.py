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


class FetchFromServiceException(Exception):
    def __init__(self, execution_point: ServiceKey, url: str = None, additional_info: str = None):
        self.status = "error"
        self.reason = f"Connection error when attempting to fetch {execution_point} from {url}"
        if additional_info:
            self.reason += additional_info


class BadUriException(Exception):
    def __init__(self, execution_point: ServiceKey, url: str = None):
        self.reason = f"Attempt to fetch {execution_point} from {url}"


def encode_for_sparql(string: str):
    trim_str = string.strip()
    return trim_str \
        .replace(" ", "%20") \
        .replace("<", "%3C") \
        .replace(">", "%3E") \
        .replace("(", "%28") \
        .replace(")", "%29") \
        .replace("{", "%7B") \
        .replace("}", "%7D") \
        .replace("'", "%27") \
        .replace("*", "%2A").replace("\\", "\\\\")


DCT_PREFIX = "PREFIX dct: <http://purl.org/dc/terms/>"
FOAF_PREFIX = "PREFIX foaf: <http://xmlns.com/foaf/0.1/>"
OWL_PREFIX = "PREFIX owl: <http://www.w3.org/2002/07/owl%23>"


def aggregation_cache(function):
    memo = {}

    def wrapper(organizations_from_service, concepts, datasets, dataservices,
                informationmodels):
        content_hash = hash(tuple([x for x in concepts + datasets + dataservices + informationmodels]))
        if content_hash in memo:
            return memo[content_hash]
        else:
            rv = function(organizations_from_service, concepts, datasets, dataservices, informationmodels)
            memo[content_hash] = rv
            return rv

    return wrapper


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
    SRC_ORGANIZATION = "publisher"
    FORMAT = "format"
    WITH_SUBJECT = "withSubject"
    OPEN_DATA = "opendata"
    TOTAL = "total"
    NEW_LAST_WEEK = "new_last_week"
    NATIONAL_COMPONENT = "nationalComponent"
    ORGANIZATION = "organization"
    COUNT = "count"
    VALUE = "value"
    ACCESS_RIGHTS_CODE = "code"
    TIME_SERIES_MONTH = "month"
    TIME_SERIES_YEAR = "year"
    TIME_SERIES_Y_AXIS = "yAxis"
    TIME_SERIES_X_AXIS = "xAxis"
    THEME = "theme"
    ORG_NAME = "name"
    ORGANIZATION_URI = "organization"
    LOS_PATH = "losPath"
    CATALOGS = "catalogs"
    ORGANIZATION_COUNT = "organizationCount"


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

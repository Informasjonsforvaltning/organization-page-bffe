import os


class ServiceKey:
    ORGANIZATIONS = "organizations"
    INFO_MODELS = "informationmodels"
    DATA_SERVICES = "dataservices"
    OLD_DATA_SERVICES = "apis"
    DATA_SETS = "datasets"
    CONCEPTS = "concepts"


class FetchFromServiceException(Exception):
    def __init__(self, execution_point: ServiceKey, url: str = None):
        self.status = "error"
        self.reason = f"Connection error when attempting to fetch {execution_point} from {url}"


class BadUriException(Exception):
    def __init__(self, execution_point: ServiceKey, url: str = None):
        self.reason = f"Attempt to fetch {execution_point} from {url}"


def build_dataset_sparql_query():
    prefixes = f"{DCT_PREFIX}{FOAF_PREFIX} {OWL_PREFIX} "
    select_fields = "?uri ?name (COUNT(?item) AS ?count)"
    nested_select_fields = "?publisher ?uri ?name"
    publisher_a_agent = "?publisher a foaf:Agent ."
    item_a_publisher = "?item dct:publisher ?publisher ."
    publisher_name = "{ ?publisher foaf:name ?name . }"
    publisher_same_as = "{ ?publisher owl:sameAs ?sameAs . }"
    bind_sameAs_as_uri = "(COALESCE(?sameAs, STR(?publisher)) AS ?uri)"
    start_nested = "{"
    end_nested = "}"
    start_where = "{"
    end_where = "}"
    group_by = "?uri ?name"
    order_by = "DESC(?count)"

    return f"{prefixes}" \
           f"SELECT {select_fields} " \
           f"WHERE {start_where} {publisher_a_agent} {item_a_publisher} " \
           f"{start_nested} SELECT {nested_select_fields}" \
           f" WHERE {start_where} {publisher_a_agent} " \
           f"OPTIONAL {publisher_name} " \
           f"OPTIONAL {publisher_same_as} " \
           f"BIND{bind_sameAs_as_uri}" \
           f" {end_where}" \
           f" {end_nested}" \
           f" {end_where} " \
           f"GROUP BY {group_by} " \
           f"ORDER BY {order_by}"


def encode_for_sparql(string: str):
    return string \
        .replace(" ", "%20") \
        .replace("<", "%3C") \
        .replace(">", "%3E") \
        .replace("(", "%28") \
        .replace(")", "%29")


DCT_PREFIX = "PREFIX dct: <http://purl.org/dc/terms/>"
FOAF_PREFIX = "PREFIX foaf: <http://xmlns.com/foaf/0.1/>"
OWL_PREFIX = "PREFIX owl: <http://www.w3.org/2002/07/owl%23>"
sparql_queries = {
    ServiceKey.DATA_SETS: build_dataset_sparql_query()
}


def aggregation_cache(function):
    memo = {}

    def wrapper(organizations_from_service, concepts, datasets, dataservices,
                informationmodels):
        content_hash = hash(tuple([x for x in concepts + datasets + dataservices + informationmodels]))
        if content_hash in memo:
            return memo[content_hash]
        else:
            print("new aggregation")
            rv = function(organizations_from_service, concepts, datasets, dataservices, informationmodels)
            memo[content_hash] = rv
            return rv
    return wrapper


env_variables = {
    ServiceKey.ORGANIZATIONS: 'ORGANIZATION_CATALOG_URL',
    ServiceKey.INFO_MODELS: 'INFORMATIONMODELS_HARVESTER_URL',
    ServiceKey.DATA_SERVICES: 'DATASERVICE_HARVESTER_URL',
    ServiceKey.DATA_SETS: 'DATASET_HARVESTER_URL',
    ServiceKey.CONCEPTS: 'CONCEPT_HARVESTER_URL'
}


def get_service_urls(service: ServiceKey):
    base_url = os.getenv(env_variables[service]) or "http://localhost:8080"
    if service == ServiceKey.DATA_SETS:
        return base_url
    elif service == ServiceKey.DATA_SERVICES:
        return f"{base_url}/{ServiceKey.OLD_DATA_SERVICES}"
    else:
        return f"{base_url}/{service}"


service_urls = {
    ServiceKey.ORGANIZATIONS: get_service_urls(ServiceKey.ORGANIZATIONS),
    ServiceKey.INFO_MODELS: get_service_urls(ServiceKey.INFO_MODELS),
    ServiceKey.DATA_SERVICES: get_service_urls(ServiceKey.DATA_SERVICES),
    ServiceKey.DATA_SETS: get_service_urls(ServiceKey.DATA_SETS),
    ServiceKey.CONCEPTS: get_service_urls(ServiceKey.CONCEPTS)

}

service_ready_urls = {
    ServiceKey.ORGANIZATIONS: f"{os.getenv('ORGANIZATION_CATALOG_URL')}/ready" or "http://localhost:8080/ready",
    ServiceKey.INFO_MODELS: get_service_urls(ServiceKey.INFO_MODELS),
    ServiceKey.DATA_SERVICES: get_service_urls(ServiceKey.DATA_SERVICES),
    ServiceKey.DATA_SETS: get_service_urls(ServiceKey.DATA_SETS),
    ServiceKey.CONCEPTS: get_service_urls(ServiceKey.CONCEPTS)
}

class ServiceKey:
    ORGANIZATIONS = "organization"
    INFO_MODELS = "informationmodels"
    DATA_SERVICES = "dataservices"
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
    """"""
    encoding = {
        " ": "%20",
        "<": "%3C",
        ">": "%3E",
        "(": "%28",
        ")": "%29",
    }
    return string \
        .replace(" ", "%20") \
        .replace("<", "%3C") \
        .replace(">", "%3E") \
        .replace("(", "%28") \
        .replace(")", "%29")


hasjk = """PREFIX dct: <http://purl.org/dc/terms/>PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX owl: <http://www.w3.org/2002/07/owl%23>
SELECT ?uri ?name (COUNT(?item) AS ?count)
WHERE {
  ?publisher a foaf:Agent .
  ?item dct:publisher ?publisher .
  {
    SELECT ?publisher ?uri ?name
    WHERE {
      ?publisher a foaf:Agent .
      OPTIONAL {
        ?publisher foaf:name ?name .
      }
      OPTIONAL {
        ?publisher owl:sameAs ?sameAs .
      }
      BIND(COALESCE(?sameAs, STR(?publisher)) AS ?uri)
    }
  }
}
GROUP BY ?uri ?name
ORDER BY DESC(?count)"""

DCT_PREFIX = "PREFIX dct: <http://purl.org/dc/terms/>"
FOAF_PREFIX = "PREFIX foaf: <http://xmlns.com/foaf/0.1/>"
OWL_PREFIX = "PREFIX owl: <http://www.w3.org/2002/07/owl%23>"
sparql_queries = {
    ServiceKey.DATA_SETS: build_dataset_sparql_query()
}

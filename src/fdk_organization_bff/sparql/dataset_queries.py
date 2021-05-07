"""Module for Dataset SPARQL-queries."""
from string import Template


def build_org_datasets_query(organization_id: str) -> str:
    """Build query for an organizations datasets."""
    query_template = Template(
        """
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX dcat: <http://www.w3.org/ns/dcat#>
PREFIX fdk: <https://raw.githubusercontent.com/Informasjonsforvaltning/fdk-data-transformation-service/master/src/main/resources/ontology/fdk.owl#>

SELECT DISTINCT ?dataset ?issued ?isAuthoritative ?isOpenData
FROM <https://datasets.fellesdatakatalog.digdir.no>
WHERE {{
    ?dataset a dcat:Dataset .
    ?record foaf:primaryTopic ?dataset .
    ?record dct:issued ?issued .
    OPTIONAL {{ ?dataset fdk:isOpenData ?isOpenData . }}
    OPTIONAL {{ ?dataset fdk:isAuthoritative ?isAuthoritative . }}
    ?catalog dcat:dataset ?dataset .
    OPTIONAL {{ ?dataset dct:publisher ?dsPublisher . }}
    OPTIONAL {{ ?catalog dct:publisher ?catPublisher . }}
    BIND ( IF( EXISTS {{ ?dataset dct:publisher ?dsPublisher . }},
        ?dsPublisher, ?catPublisher ) AS ?publisher ) .
    ?publisher dct:identifier "$org_id" .
}}"""
    )

    return query_template.substitute(org_id=organization_id)


def build_nap_org_datasets_query(organization_id: str) -> str:
    """Build query for an organizations NAP datasets."""
    query_template = Template(
        """
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX dcat: <http://www.w3.org/ns/dcat#>
PREFIX fdk: <https://raw.githubusercontent.com/Informasjonsforvaltning/fdk-data-transformation-service/master/src/main/resources/ontology/fdk.owl#>

SELECT DISTINCT ?dataset ?issued ?isAuthoritative ?isOpenData
FROM <https://datasets.fellesdatakatalog.digdir.no>
WHERE {{
    ?dataset a dcat:Dataset .
    ?dataset fdk:isRelatedToTransportportal ?isNAP .
    FILTER (STR(?isNAP) = "true")
    ?record foaf:primaryTopic ?dataset .
    ?record dct:issued ?issued .
    OPTIONAL {{ ?dataset fdk:isOpenData ?isOpenData . }}
    OPTIONAL {{ ?dataset fdk:isAuthoritative ?isAuthoritative . }}
    ?catalog dcat:dataset ?dataset .
    OPTIONAL {{ ?dataset dct:publisher ?dsPublisher . }}
    OPTIONAL {{ ?catalog dct:publisher ?catPublisher . }}
    BIND ( IF( EXISTS {{ ?dataset dct:publisher ?dsPublisher . }},
        ?dsPublisher, ?catPublisher ) AS ?publisher ) .
    ?publisher dct:identifier "$org_id" .
}}"""
    )

    return query_template.substitute(org_id=organization_id)


def build_datasets_by_publisher_query() -> str:
    """Build query to count datasets grouped by publisher."""
    return """
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX dcat: <http://www.w3.org/ns/dcat#>
SELECT ?organizationNumber (COUNT(DISTINCT ?dataset) AS ?count)
FROM <https://datasets.fellesdatakatalog.digdir.no>
WHERE {{
    ?dataset a dcat:Dataset .
    ?catalog dcat:dataset ?dataset .
    OPTIONAL {{ ?dataset dct:publisher ?dsPublisher . }}
    OPTIONAL {{ ?catalog dct:publisher ?catPublisher . }}
    BIND ( IF( EXISTS {{ ?dataset dct:publisher ?dsPublisher . }},
        ?dsPublisher, ?catPublisher ) AS ?publisher ) .
    ?publisher dct:identifier ?organizationNumber .
}}
GROUP BY ?organizationNumber"""


def build_nap_datasets_by_publisher_query() -> str:
    """Build query to count NAP datasets grouped by publisher."""
    return """
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX dcat: <http://www.w3.org/ns/dcat#>
PREFIX fdk: <https://raw.githubusercontent.com/Informasjonsforvaltning/fdk-data-transformation-service/master/src/main/resources/ontology/fdk.owl#>

SELECT ?organizationNumber (COUNT(DISTINCT ?dataset) AS ?count)
FROM <https://datasets.fellesdatakatalog.digdir.no>
WHERE {{
    ?dataset a dcat:Dataset .
    ?dataset fdk:isRelatedToTransportportal ?isNAP .
    FILTER (STR(?isNAP) = "true")
    ?catalog dcat:dataset ?dataset .
    OPTIONAL {{ ?dataset dct:publisher ?dsPublisher . }}
    OPTIONAL {{ ?catalog dct:publisher ?catPublisher . }}
    BIND ( IF( EXISTS {{ ?dataset dct:publisher ?dsPublisher . }},
        ?dsPublisher, ?catPublisher ) AS ?publisher ) .
    ?publisher dct:identifier ?organizationNumber .
}}
GROUP BY ?organizationNumber"""

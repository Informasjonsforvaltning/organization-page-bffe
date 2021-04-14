"""Module for SPARQL-queries."""
from string import Template

from fdk_organization_bff.config import Config


def build_org_datasets_query(organization_id: str) -> str:
    """Build query for an organizations datasets."""
    query_template = Template(
        """
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX dcat: <http://www.w3.org/ns/dcat#>

SELECT DISTINCT ?dataset ?issued ?provenance ?rights ?licenseSource
FROM <https://datasets.fellesdatakatalog.digdir.no>
WHERE {{
    ?dataset a dcat:Dataset .
    ?record foaf:primaryTopic ?dataset .
    ?record dct:issued ?issued .
    OPTIONAL {{ ?dataset dct:provenance ?provenance . }}
    OPTIONAL {{ ?dataset dct:accessRights ?rights . }}
    OPTIONAL {{
        ?dataset dcat:distribution ?distribution .
        ?distribution dct:license ?license .
        OPTIONAL {{ ?license dct:source ?source . }}
        BIND ( IF( EXISTS {{ ?license dct:source ?source . }},
            ?source, ?license ) AS ?licenseSource ) .
    }}
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

SELECT DISTINCT ?dataset ?issued ?provenance ?rights ?licenseSource
FROM <https://datasets.fellesdatakatalog.digdir.no>
WHERE {{
    ?dataset a dcat:Dataset .
    ?record foaf:primaryTopic ?dataset .
    ?record dct:issued ?issued .
    OPTIONAL {{ ?dataset dct:provenance ?provenance . }}
    ?dataset dct:accessRights ?rights .
    FILTER (STR(?rights) = "http://publications.europa.eu/resource/authority/access-right/PUBLIC")
    OPTIONAL {{
        ?dataset dcat:distribution ?distribution .
        ?distribution dct:license ?license .
        OPTIONAL {{ ?license dct:source ?source . }}
        BIND ( IF( EXISTS {{ ?license dct:source ?source . }},
            ?source, ?license ) AS ?licenseSource ) .
    }}
    ?catalog dcat:dataset ?dataset .
    OPTIONAL {{ ?dataset dct:publisher ?dsPublisher . }}
    OPTIONAL {{ ?catalog dct:publisher ?catPublisher . }}
    BIND ( IF( EXISTS {{ ?dataset dct:publisher ?dsPublisher . }},
        ?dsPublisher, ?catPublisher ) AS ?publisher ) .
    ?publisher dct:identifier "$org_id" .
    ?dataset dcat:theme ?theme .
    FILTER (STR(?theme) IN ( $nap_themes ))
}}"""
    )

    return query_template.substitute(
        org_id=organization_id, nap_themes=",".join(Config.nap_themes())
    )


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
    query_template = Template(
        """
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
    ?dataset dct:accessRights ?rights .
    FILTER (STR(?rights) = "http://publications.europa.eu/resource/authority/access-right/PUBLIC")
    ?dataset dcat:theme ?theme .
    FILTER (STR(?theme) IN ( $nap_themes ) )
}}
GROUP BY ?organizationNumber"""
    )

    return query_template.substitute(nap_themes=",".join(Config.nap_themes()))


def build_dataservices_by_publisher_query() -> str:
    """Build query to count dataservices grouped by publisher."""
    return """
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX dcat: <http://www.w3.org/ns/dcat#>
SELECT ?organizationNumber (COUNT(DISTINCT ?service) AS ?count)
FROM <https://dataservices.fellesdatakatalog.digdir.no>
WHERE {{
    ?service a dcat:DataService .
    ?catalog dcat:service ?service .
    OPTIONAL {{ ?service dct:publisher ?servicePublisher . }}
    OPTIONAL {{ ?catalog dct:publisher ?catPublisher . }}
    BIND ( IF( EXISTS {{ ?service dct:publisher ?servicePublisher . }},
        ?servicePublisher, ?catPublisher ) AS ?publisher ) .
    ?publisher dct:identifier ?organizationNumber .
}}
GROUP BY ?organizationNumber"""

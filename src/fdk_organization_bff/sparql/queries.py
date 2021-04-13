"""Module for SPARQL-queries."""
from string import Template


def build_org_datasets_query(organization_id: str) -> str:
    """Build query for an organizations datasets."""
    query_template = Template(
        """
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX dcat: <http://www.w3.org/ns/dcat#>

SELECT ?dataset ?issued ?provenance ?rights ?licenseSource
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
        ?license dct:source ?licenseSource .
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

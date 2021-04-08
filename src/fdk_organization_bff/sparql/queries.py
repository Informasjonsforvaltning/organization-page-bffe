"""Module for SPARQL-queries."""
from string import Template
from urllib.parse import quote_plus


def build_org_datasets_query(organization_id: str) -> str:
    """Build urlencoded query for an organizations datasets."""
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

    return quote_plus(query_template.substitute(org_id=organization_id))
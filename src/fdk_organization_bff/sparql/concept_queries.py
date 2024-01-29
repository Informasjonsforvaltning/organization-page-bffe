"""Module for Concept SPARQL-queries."""

from string import Template


def build_concepts_by_publisher_query() -> str:
    """Build query to count concepts grouped by publisher."""
    return """
        PREFIX dct: <http://purl.org/dc/terms/>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT ?organizationNumber (COUNT(DISTINCT ?concept) AS ?count)
        FROM <https://concepts.fellesdatakatalog.digdir.no>
        WHERE {{
            ?concept a skos:Concept .
            ?concept dct:publisher ?publisher .
            ?publisher dct:identifier ?organizationNumber .
        }}
        GROUP BY ?organizationNumber
    """


def build_org_concepts_query(organization_id: str) -> str:
    """Build query for an organizations concepts."""
    return Template(
        """
        PREFIX dct: <http://purl.org/dc/terms/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT DISTINCT ?concept ?issued
        FROM <https://concepts.fellesdatakatalog.digdir.no>
        WHERE {{
            ?concept a skos:Concept .
            ?record foaf:primaryTopic ?concept .
            ?record dct:issued ?issued .
            ?concept dct:publisher ?publisher .
            ?publisher dct:identifier "$org_id" .
        }}
    """
    ).substitute(org_id=organization_id)

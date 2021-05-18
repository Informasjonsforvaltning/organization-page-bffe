"""Module for Concept SPARQL-queries."""


def build_concepts_by_publisher_query() -> str:
    """Build query to count dataservices grouped by publisher."""
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
GROUP BY ?organizationNumber"""

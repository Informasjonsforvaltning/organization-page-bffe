"""Module for Information Model SPARQL-queries."""


def build_informationmodels_by_publisher_query() -> str:
    """Build query to count dataservices grouped by publisher."""
    return """
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#>
SELECT ?organizationNumber (COUNT(DISTINCT ?model) AS ?count)
FROM <https://informationmodels.fellesdatakatalog.digdir.no>
WHERE {{
    ?model a modelldcatno:InformationModel .
    ?model dct:publisher ?publisher .
    ?publisher dct:identifier ?organizationNumber .
}}
GROUP BY ?organizationNumber"""

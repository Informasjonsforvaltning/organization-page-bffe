def build_dataset_publisher_query() -> str:
    return """
        PREFIX dct: <http://purl.org/dc/terms/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX dcat: <http://www.w3.org/ns/dcat#>

        SELECT ?organizationNumber (COUNT(DISTINCT ?item) AS ?count)
        FROM <https://datasets.fellesdatakatalog.digdir.no>
        WHERE {{
            ?item a dcat:Dataset .
            ?item dct:publisher ?publisher .
            ?publisher a foaf:Agent .
            ?publisher dct:identifier ?organizationNumber .
        }}
        GROUP BY ?organizationNumber
    """


def build_dataset_publisher_query_for_transportportal() -> str:
    return f"""
        PREFIX dct: <http://purl.org/dc/terms/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX dcat: <http://www.w3.org/ns/dcat#>

        SELECT ?organizationNumber (COUNT(DISTINCT ?item) AS ?count)
        FROM <https://datasets.fellesdatakatalog.digdir.no>
        WHERE {{
            ?publisher a foaf:Agent .
            ?publisher dct:identifier ?organizationNumber .
            ?item a dcat:Dataset .
            ?item dct:publisher ?publisher .
            OPTIONAL {{ ?item dct:accessRights ?code . }}
            OPTIONAL {{ ?item dcat:theme ?theme . }}
            FILTER EXISTS {{ ?item dct:accessRights ?code . }}
            FILTER EXISTS {{ ?item dcat:theme ?theme . }}
            FILTER (STR(?code) = "http://publications.europa.eu/resource/authority/access-right/PUBLIC")
            FILTER (STR(?theme) IN (
                    "https://psi.norge.no/los/tema/mobilitetstilbud",
                    "https://psi.norge.no/los/tema/trafikkinformasjon",
                    "https://psi.norge.no/los/tema/veg-og-vegregulering",
                    "https://psi.norge.no/los/tema/yrkestransport"
                )
            )
        }}
        GROUP BY ?organizationNumber
    """


def build_dataservices_publisher_query() -> str:
    return """
        PREFIX dct: <http://purl.org/dc/terms/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX dcat: <http://www.w3.org/ns/dcat#>

        SELECT ?organizationNumber (COUNT(DISTINCT ?service) AS ?count)
        WHERE {{
            ?catalog dcat:service ?service .
            ?catalog dct:publisher ?publisher .
            ?publisher a foaf:Agent .
            ?publisher dct:identifier ?organizationNumber .
        }}
        GROUP BY ?organizationNumber
    """

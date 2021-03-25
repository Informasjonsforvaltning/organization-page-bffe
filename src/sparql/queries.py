def build_dataset_publisher_query() -> str:
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
        GROUP BY ?organizationNumber
    """


def build_dataset_publisher_query_for_transportportal() -> str:
    return f"""
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
            OPTIONAL {{ ?dataset dct:accessRights ?code . }}
            OPTIONAL {{ ?dataset dcat:theme ?theme . }}
            FILTER EXISTS {{ ?dataset dct:accessRights ?code . }}
            FILTER EXISTS {{ ?dataset dcat:theme ?theme . }}
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
        GROUP BY ?organizationNumber
    """

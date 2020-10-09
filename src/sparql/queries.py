from src.sparql.builder import FromGraph, SparqlSelect, SparqlWhere, SparqlGraphTerm, SparqlOptional, \
    SparqlBuilder, SparqlFunction
from src.sparql.rdf_namespaces import NamespaceProperty, DCT, FOAF, OWL, SparqlFunctionString, DCAT
from src.utils import ContentKeys


def build_dataset_publisher_query() -> str:
    return """
        PREFIX dct: <http://purl.org/dc/terms/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX dcat: <http://www.w3.org/ns/dcat#>

        SELECT ?publisher ?sameAs ?name ?organisationNumber (COUNT(?item) AS ?count)
        FROM <https://datasets.fellesdatakatalog.digdir.no>
        WHERE {{
            ?publisher a foaf:Agent .
            ?publisher foaf:name ?name .
            ?publisher dct:identifier ?organisationNumber .
            ?item a dcat:Dataset .
            ?item dct:publisher ?publisher .
            OPTIONAL {{
                ?publisher owl:sameAs ?sameAs .
            }}
        }}
        GROUP BY ?publisher ?name ?sameAs ?organisationNumber
    """


def build_dataset_publisher_query_for_transportportal() -> str:
    return f"""
        PREFIX dct: <http://purl.org/dc/terms/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX dcat: <http://www.w3.org/ns/dcat#>

        SELECT ?publisher ?sameAs ?name ?organizationNumber (COUNT(?item) AS ?count)
        FROM <https://datasets.fellesdatakatalog.digdir.no>
        WHERE {{
            ?publisher a foaf:Agent .
            ?publisher foaf:name ?name .
            ?publisher dct:identifier ?organizationNumber .
            ?item a dcat:Dataset .
            ?item dct:publisher ?publisher .
            OPTIONAL {{ ?publisher owl:sameAs ?sameAs . }}
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
        GROUP BY ?publisher ?name ?sameAs ?organizationNumber
    """


def build_dataservices_publisher_query() -> str:
    dct = DCT(NamespaceProperty.TTL)
    foaf = FOAF(NamespaceProperty.TTL)
    owl = OWL(NamespaceProperty.TTL)
    dcat = DCAT(NamespaceProperty.TTL)

    catalog_var = "catalog"
    service_var = "service"
    catalog_graph_term = SparqlGraphTerm(var=catalog_var)
    publisher_graph_term = SparqlGraphTerm(var=ContentKeys.PUBLISHER)

    prefixes = [dct, foaf, owl, dcat]
    select = SparqlSelect(
        variable_names=[ContentKeys.PUBLISHER, ContentKeys.SAME_AS],
        functions=[
            SparqlFunction(
                function=SparqlFunctionString.COUNT,
                var=service_var,
                as_var=ContentKeys.COUNT
            )
        ],
        from_graph=FromGraph.DATA_SERVICES
    )
    catalog_dct_publisher = SparqlGraphTerm.build_graph_pattern(
        subject=catalog_graph_term,
        predicate=SparqlGraphTerm(namespace_property=dct.publisher),
        obj=publisher_graph_term,
        close_pattern_with="."
    )
    catalog_dcat_service = SparqlGraphTerm.build_graph_pattern(
        subject=catalog_graph_term,
        predicate=SparqlGraphTerm(namespace_property=dcat.service),
        obj=SparqlGraphTerm(var=service_var),
        close_pattern_with="."
    )
    optional_publisher_same_as = SparqlOptional(
        graphs=[
            SparqlGraphTerm.build_graph_pattern(
                subject=SparqlGraphTerm(var=ContentKeys.PUBLISHER),
                predicate=SparqlGraphTerm(namespace_property=owl.sameAs),
                obj=SparqlGraphTerm(var=ContentKeys.SAME_AS),
                close_pattern_with="."
            )
        ]
    )

    where = SparqlWhere(
        graphs=[catalog_dct_publisher, catalog_dcat_service],
        optional=optional_publisher_same_as
    )

    return SparqlBuilder(
        prefix=prefixes,
        select=select,
        where=where,
        group_by_vars=[ContentKeys.PUBLISHER, ContentKeys.SAME_AS]
    ).build()

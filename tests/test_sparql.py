import pytest

from src.sparql.builder import SparqlFunction, SparqlSelect, SparqlGraphTerm, SparqlWhere, SparqlOptional, SparqlBuilder
from src.sparql.queries import build_dataservices_publisher_query
from src.sparql.rdf_namespaces import SparqlFunctionString, FOAF, NamespaceProperty, RDF, OWL


@pytest.mark.unit
def test_build_dataservice_publisher_query():
    expected = "PREFIX dct: <http://purl.org/dc/terms/> " \
               "PREFIX foaf: <http://xmlns.com/foaf/0.1/> " \
               "PREFIX owl: <http://www.w3.org/2002/07/owl#> " \
               "PREFIX dcat: <http://www.w3.org/ns/dcat#> " \
               "SELECT ?publisher ?sameAs (COUNT(?service) AS ?count) " \
               "FROM <https://dataservices.fellesdatakatalog.digdir.no> " \
               "WHERE { " \
               "?catalog dct:publisher ?publisher . " \
               "?catalog dcat:service ?service . " \
               "OPTIONAL { ?publisher owl:sameAs ?sameAs . } } " \
               "GROUP BY ?publisher ?sameAs"

    result = build_dataservices_publisher_query()
    assert result == expected


@pytest.mark.unit
def test_sparql_count_function():
    result = SparqlFunction(function=SparqlFunctionString.COUNT, var="something", as_var="count")
    assert str(result) == "COUNT(?something) AS ?count"


@pytest.mark.unit
def test_sparql_select():
    result_vars_only = SparqlSelect(variable_names=["one", "two"])
    assert str(result_vars_only) == "SELECT ?one ?two"

    result_with_count_function = SparqlSelect(
        variable_names=["one", "three"],
        functions=[
            SparqlFunction(function=SparqlFunctionString.COUNT,
                           var="five",
                           as_var="five_count")
        ]
    )

    assert str(result_with_count_function) == "SELECT ?one ?three (COUNT(?five) AS ?five_count)"


@pytest.mark.unit
def test_sparql_where():
    foaf = FOAF(NamespaceProperty.TTL)
    rdf = RDF(NamespaceProperty.TTL)
    owl = OWL(NamespaceProperty.TTL)

    expected = "WHERE { ?publisher a foaf:Agent . OPTIONAL { ?publisher owl:sameAs ?sameAs . }"
    publisher_a_foaf_agent = SparqlGraphTerm.build_graph_pattern(
        subject=SparqlGraphTerm(var="?publisher"),
        predicate=SparqlGraphTerm(namespace_property=rdf.type),
        obj=SparqlGraphTerm(namespace_property=foaf.agent),
        close_pattern_with="."
    )
    optional_publisher_same_as = SparqlOptional(
        graphs=[
            SparqlGraphTerm.build_graph_pattern(
                subject=SparqlGraphTerm(var="publisher"),
                predicate=SparqlGraphTerm(namespace_property=owl.sameAs),
                obj=SparqlGraphTerm(var="sameAs"),
                close_pattern_with="."
            )
        ]
    )

    result = SparqlWhere(
        graphs=[publisher_a_foaf_agent],
        optional=optional_publisher_same_as
    )

    assert str(result) == expected


@pytest.mark.unit
def test_sparql_build():
    expected = "PREFIX foaf: <http://xmlns.com/foaf/0.1/> PREFIX owl: <http://www.w3.org/2002/07/owl#> " \
               "SELECT ?publisher (COUNT(?sameAs) AS ?count) " \
               "WHERE { ?publisher a foaf:Agent . OPTIONAL { ?publisher owl:sameAs ?sameAs . } } " \
               "GROUP BY ?publisher"

    select_with_count_function = SparqlSelect(
        variable_names=["publisher"],
        functions=[
            SparqlFunction(function=SparqlFunctionString.COUNT,
                           var="sameAs",
                           as_var="count")
        ]
    )

    foaf = FOAF(NamespaceProperty.TTL)
    rdf = RDF(NamespaceProperty.TTL)
    owl = OWL(NamespaceProperty.TTL)

    publisher_a_foaf_agent = SparqlGraphTerm.build_graph_pattern(
        subject=SparqlGraphTerm(var="?publisher"),
        predicate=SparqlGraphTerm(namespace_property=rdf.type),
        obj=SparqlGraphTerm(namespace_property=foaf.agent),
        close_pattern_with="."
    )
    optional_publisher_same_as = SparqlOptional(
        graphs=[
            SparqlGraphTerm.build_graph_pattern(
                subject=SparqlGraphTerm(var="publisher"),
                predicate=SparqlGraphTerm(namespace_property=owl.sameAs),
                obj=SparqlGraphTerm(var="sameAs"),
                close_pattern_with="."
            )
        ]
    )

    where_with_optional = SparqlWhere(
        graphs=[publisher_a_foaf_agent],
        optional=optional_publisher_same_as
    )

    result = SparqlBuilder(
        prefix=[foaf, owl],
        select=select_with_count_function,
        where=where_with_optional,
        group_by_vars=["publisher"]
    )

    assert result.build() == expected

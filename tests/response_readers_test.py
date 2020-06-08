import os

import pytest

from src.response_readers import ParsedResult, read_sparql_table, read_sparql_row


@pytest.mark.unit
def test_result_with_norwegian_registry_reference():
    result = ParsedResult(count=5, organizationIri="http://data.brreg.no/enhetsregisteret/enhet/971040238", name=None)
    assert result.count == 5
    assert result.norwegianRegistry_iri == "http://data.brreg.no/enhetsregisteret/enhet/971040238"
    assert hasattr(result, 'alternativeRegistry_iri') is False


@pytest.mark.unit
def test_result_with_alternative_known_registry_reference():
    result = ParsedResult(count=5,
                          organizationIri="https://register.geonorge.no/7ac1627a-2e25-4dad-9213-c04a15a462e4",
                          name="osijh")
    assert result.alternativeRegistry_iri == "https://register.geonorge.no/7ac1627a-2e25-4dad-9213-c04a15a462e4"
    assert hasattr(result, 'norwegianRegistry_iri') is False
    assert hasattr(result, 'name') is True


@pytest.mark.unit
def test_result_with_unknown_registry_reference_should_throw_error_then_return_result():
    result = ParsedResult(count=76, organizationIri="http://non.authorative/registry/19635686", name="iooy")
    assert result.alternativeRegistry_iri == "http://non.authorative/registry/19635686"
    assert result.count == 76
    assert hasattr(result, 'norwegianRegistry_iri') is False
    assert hasattr(result, 'name') is True


@pytest.mark.unit
def test_read_sparql_table_should_return_result_with_norwegian_registry():
    sparql_table = open(os.getcwd() + '/data/2_datasets_norwegian_registry').read()
    result = read_sparql_table(sparql_table)
    assert result.__len__() == 2
    assert result[0].__dict__ == ParsedResult(count=643,
                                     organizationIri="https://data.brreg.no/enhetsregisteret/api/enheter/910298062",
                                     name="KARMSUND OG KYSNESSTRAND REVISJON").__dict__
    assert result[1].__dict__ == ParsedResult(count=109,
                                     organizationIri="http://data.brreg.no/enhetsregisteret/enhet/971040238",
                                     name="Kartverket"
                                     ).__dict__


@pytest.mark.unit
def test_read_sparql_row_reader_should_return_result_with_norwegian_registry():
    sparql_row = '| "https://data.brreg.no/enhetsregisteret/api/enheter/910298062"                                  ' \
                 ' | "KARMSUND OG KYSNESSTRAND REVISJON"               | 643   | '
    result = read_sparql_row(sparql_row)
    assert result.count == 643
    assert result.norwegianRegistry_iri == "https://data.brreg.no/enhetsregisteret/api/enheter/910298062"


@pytest.mark.unit
def test_sparql_row_reader_should_return_result_with_alternative_registry_and_name():
    sparql_row = '| "https://someotherregistry/910298062"                                  ' \
                 ' | "Stranda Sag og Høvleri"               | 77   | '
    result = read_sparql_row(sparql_row)
    assert result.count == 77
    assert result.alternativeRegistry_iri == "https://someotherregistry/910298062"
    assert result.name == "Stranda Sag og Høvleri"

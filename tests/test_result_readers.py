import os

import pytest

from src.result_readers import ParsedContent, read_sparql_table, read_sparql_row, parse_es_results, group_by_org_uri, \
    group_by_org_id, read_alt_organization_rdf_xml
from tests.test_data import geonorge_rdf_organization, parsed_org_from_geonorge


@pytest.mark.unit
def test_result_with_norwegian_registry_reference():
    result = ParsedContent(count=5, org_id="http://data.brreg.no/enhetsregisteret/enhet/971040238",
                           name=None)
    assert result.count == 5
    assert result.norwegianRegistry_iri == "http://data.brreg.no/enhetsregisteret/enhet/971040238"
    assert hasattr(result, 'alternativeRegistry_iri') is False


@pytest.mark.unit
def test_result_with_norwegian_registry_reference_equals_iri():
    result = ParsedContent(count=5, org_id="http://data.brreg.no/enhetsregisteret/enhet/971040238",
                           name=None)
    assert result == ParsedContent(count=20, org_id="http://data.brreg.no/enhetsregisteret/enhet/971040238",
                                   name=None)
    assert result == ParsedContent(count=5, org_id="https://data.brreg.no/enhetsregisteret/enhet/971040238",
                                   name=None)
    assert result == "http://data.brreg.no/enhetsregisteret/enhet/971040238"
    assert result == "http://data.brreg.no/enhetsregisteret/enhet/971040238"
    assert result == "971040238"
    assert result != ParsedContent(count=5, org_id="http://data.brreg.no/enhetsregisteret/enhet/971040298",
                                   name=None)
    assert result != ParsedContent(count=5,
                                   org_id="https://register.geonorge.no/7ac1627a-2e25-4dad-9213-c04a15a462e4",
                                   name="osijh")
    assert result != ParsedContent(count=5,
                                   org_id="NAME",
                                   name="NAME")
    assert result != "https://data.brreg.no/enhetsregisteret/enhet/971046239"
    assert result != "http://data.brreg.no/enhetsregisteret/enhet/9710402639"
    assert result != "971040239"


@pytest.mark.unit
def test_result_with_organization_registry_reference_equals_orgid():
    result = ParsedContent(count=5, org_id="971040238", name=None)
    assert result == ParsedContent(count=20, org_id="971040238",
                                   name=None)
    assert result == ParsedContent(count=5, org_id="http://data.brreg.no/enhetsregisteret/enhet/971040238",
                                   name=None)
    assert result != ParsedContent(count=5, org_id="http://data.brreg.no/enhetsregisteret/enhet/071040238",
                                   name=None)
    assert result != ParsedContent(count=5, org_id="https://register.geonorge.no/7ac1627a-2e25-4dad-9213-c04a15a462e4",
                                   name=None)
    assert result == "971040238"
    assert result != "http://data.brreg.no/enhetsregisteret/enhet/171040238"
    assert result != "https://data.brreg.no/enhetsregisteret/enhet/1971040238"

    assert result == "http://data.brreg.no/enhetsregisteret/enhet/971040238"
    assert result == "https://data.brreg.no/enhetsregisteret/enhet/971040238"
    assert result != "9710402381"


@pytest.mark.unit
def test_result_with_alternative_known_registry_reference():
    result = ParsedContent(count=5,
                           org_id="https://register.geonorge.no/7ac1627a-2e25-4dad-9213-c04a15a462e4",
                           name="osijh")
    assert result.alternativeRegistry_iri == "https://register.geonorge.no/7ac1627a-2e25-4dad-9213-c04a15a462e4"
    assert hasattr(result, 'norwegianRegistry_iri') is False
    assert hasattr(result, 'name') is True


@pytest.mark.unit
def test_result_with_alternative_known_registry_reference():
    result = ParsedContent(count=5,
                           org_id="https://register.geonorge.no/7ac1627a-2e25-4dad-9213-c04a15a462e4",
                           name="osijh")
    assert result.alternativeRegistry_iri == "https://register.geonorge.no/7ac1627a-2e25-4dad-9213-c04a15a462e4"
    assert hasattr(result, 'norwegianRegistry_iri') is False
    assert hasattr(result, 'name') is True


@pytest.mark.unit
def test_result_with_unknown_registry_reference_should_throw_error_then_return_result():
    result = ParsedContent(count=76, org_id="http://non.authorative/registry/19635686", name="iooy")
    assert result.alternativeRegistry_iri == "http://non.authorative/registry/19635686"
    assert result.count == 76
    assert hasattr(result, 'norwegianRegistry_iri') is False
    assert hasattr(result, 'name') is True


@pytest.mark.unit
def test_result_with_alternative_registry_comparison():
    result = ParsedContent(count=5,
                           org_id="https://register.geonorge.no/7ac1627a-2e25-4dad-9213-c04a15a462e4",
                           name="osijh")
    assert result == ParsedContent(count=105,
                                   org_id="https://register.geonorge.no/7ac1627a-2e25-4dad-9213-c04a15a462e4",
                                   name="osijh")
    assert result != ParsedContent(count=105,
                                   org_id="https://register.geonorge.no/7ac1627a-2e25-4dad-9213-c04",
                                   name="osijh")
    assert result != ParsedContent(count=105,
                                   org_id="7456",
                                   name="osijh")
    assert result != ParsedContent(count=105,
                                   org_id="http://data.brreg.no/enhetsregisteret/enhet/071040238",
                                   name="osijh")
    assert result == "https://register.geonorge.no/7ac1627a-2e25-4dad-9213-c04a15a462e4"
    assert result != "https://register.geonorge.no/7ac1627a-2e25-4dad-c04a15a462e4"


@pytest.mark.unit
def test_read_sparql_table_should_return_result_with_norwegian_registry():
    base_path = os.getcwd()
    if not base_path.endswith("tests"):
        base_path = f"{base_path}/tests"
    sparql_table = open(base_path + '/data/2_datasets_norwegian_registry').read()
    result = read_sparql_table(sparql_table)
    assert result.__len__() == 2
    assert result[0] == ParsedContent(count=643,
                                      org_id="https://data.brreg.no/enhetsregisteret/api/enheter/910298062",
                                      name="KARMSUND OG KYSNESSTRAND REVISJON")
    assert result[1] == ParsedContent(count=109,
                                      org_id="http://data.brreg.no/enhetsregisteret/enhet/971040238",
                                      name="Kartverket"
                                      )


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


@pytest.mark.unit
def test_es_result_reader_should_return_list_of_parsed_organizations_with_uri():
    """Should return list of ParsedResult grouped by publisher"""
    content_by_uri = parse_es_results(es_results=[
        {
            "id": "b970c1af-ab11-4016-8e1e-090ba61d74dc",
            "prefLabel": {
                "nb": "avskiltingsdato"
            },
            "publisher": {
                "uri": "http://data.brreg.no/enhetsregisteret/enhet/974760673",
                "name": "REGISTERENHETEN I BRØNNØYSUND",
                "orgPath": "/STAT/912660680/974760673",
                "prefLabel": {
                    "no": "REGISTERENHETEN I BRØNNØYSUND"
                }
            }
        },
        {
            "id": "b970c1af-ab11-4016-8e1e-090ba61d74dc",
            "prefLabel": {
                "nb": "avskiltingsdato"
            },
            "publisher": {
                "uri": "http://data.brreg.no/enhetsregisteret/enhet/974760673",
                "name": "REGISTERENHETEN I BRØNNØYSUND",
                "orgPath": "/STAT/912660680/974760673",
                "prefLabel": {
                    "no": "REGISTERENHETEN I BRØNNØYSUND"
                }
            }
        },
        {
            "id": "b970c1af-ab11-4016-8e1e-090ba61d74dc",
            "prefLabel": {
                "nb": "avskiltingsdato"
            },
            "publisher": {
                "uri": "http://data.brreg.no/enhetsregisteret/enhet/974761076",
                "name": "SKATTEETATEN",
                "orgPath": "/STAT/972417807/974761076",
                "prefLabel": {
                    "no": "SKATTEETATEN"
                }
            }
        },
    ], with_uri=True)

    assert content_by_uri.__len__() == 2
    organization_1: ParsedContent = content_by_uri[0]
    assert organization_1.count == 2
    assert organization_1.name == "REGISTERENHETEN I BRØNNØYSUND"
    assert organization_1.norwegianRegistry_iri == "http://data.brreg.no/enhetsregisteret/enhet/974760673"
    organization_2: ParsedContent = content_by_uri[1]
    assert organization_2.count == 1
    assert organization_2.name == "SKATTEETATEN"
    assert organization_2.norwegianRegistry_iri == "http://data.brreg.no/enhetsregisteret/enhet/974761076"


@pytest.mark.unit
def test_es_result_reader_should_return_list_of_parsed_organizations_with_id():
    """Should return list of ParsedResult grouped by publisher"""
    content_by_id = parse_es_results(es_results=[
        {
            "id": "b970c1af-ab11-4016-8e1e-090ba61d74dc",
            "prefLabel": {
                "nb": "avskiltingsdato"
            },
            "publisher": {
                "id": "974760673",
                "name": "REGISTERENHETEN I BRØNNØYSUND",
                "orgPath": "/STAT/912660680/974760673",
                "prefLabel": {
                    "no": "REGISTERENHETEN I BRØNNØYSUND"
                }
            }
        },
        {
            "id": "b970c1af-ab11-4016-8e1e-090ba61d74dc",
            "prefLabel": {
                "nb": "avskiltingsdato"
            },
            "publisher": {
                "id": "974760673",
                "name": "REGISTERENHETEN I BRØNNØYSUND",
                "orgPath": "/STAT/912660680/974760673",
                "prefLabel": {
                    "no": "REGISTERENHETEN I BRØNNØYSUND"
                }
            }
        },
        {
            "id": "b970c1af-ab11-4016-8e1e-090ba61d74dc",
            "prefLabel": {
                "nb": "avskiltingsdato"
            },
            "publisher": {
                "id": "974761076",
                "name": "SKATTEETATEN",
                "orgPath": "/STAT/972417807/974761076",
                "prefLabel": {
                    "no": "SKATTEETATEN"
                }
            }
        },
    ], with_uri=False)

    assert content_by_id.__len__() == 2
    organization_1: ParsedContent = content_by_id[0]
    assert organization_1.count == 2
    assert organization_1.name == "REGISTERENHETEN I BRØNNØYSUND"
    assert organization_1.org_id == "974760673"
    organization_2: ParsedContent = content_by_id[1]
    assert organization_2.count == 1
    assert organization_2.name == "SKATTEETATEN"
    assert organization_2.org_id == "974761076"


@pytest.mark.unit
def test_group_by_org_id():
    es_results = [
        {
            "id": "b970c1af-ab11-4016-8e1e-090ba61d74dc",
            "prefLabel": {
                "nb": "avskiltingsdato"
            },
            "publisher": {
                "id": "974760673",
                "name": "REGISTERENHETEN I BRØNNØYSUND",
                "orgPath": "/STAT/912660680/974760673",
                "prefLabel": {
                    "no": "REGISTERENHETEN I BRØNNØYSUND"
                }
            }
        },
        {
            "id": "b970c1af-ab11-4016-8e1e-090ba61d74dc",
            "prefLabel": {
                "nb": "avskiltingsdato"
            },
            "publisher": {
                "id": "974760673",
                "name": "REGISTERENHETEN I BRØNNØYSUND",
                "orgPath": "/STAT/912660680/974760673",
                "prefLabel": {
                    "no": "REGISTERENHETEN I BRØNNØYSUND"
                }
            }
        },
        {
            "id": "b970c1af-ab11-4016-8e1e-090ba61d74dc",
            "prefLabel": {
                "nb": "avskiltingsdato"
            },
            "publisher": {
                "uri": "http://data.brreg.no/enhetsregisteret/enhet/974761076",
                "name": "SKATTEETATEN",
                "orgPath": "/STAT/972417807/974761076",
                "prefLabel": {
                    "no": "SKATTEETATEN"
                }
            }
        }
    ]
    result = group_by_org_id(es_results=es_results)
    assert result.__len__() == 2


@pytest.mark.unit
def test_group_by_org_uri_should_discard_entries_without_publisher():
    es_results = [
        {
            "id": "b970c1af-ab11-4016-8e1e-090ba61d74dc",
            "prefLabel": {
                "nb": "avskiltingsdato"
            }
        },
        {
            "id": "b970c1af-ab11-4016-8e1e-090ba61d74dc",
            "prefLabel": {
                "nb": "avskiltingsdato"
            },
            "publisher": {
                "uri": "http://data.brreg.no/enhetsregisteret/enhet/974760673",
                "name": "REGISTERENHETEN I BRØNNØYSUND",
                "orgPath": "/STAT/912660680/974760673",
                "prefLabel": {
                    "no": "REGISTERENHETEN I BRØNNØYSUND"
                }
            }
        },
        {
            "id": "b970c1af-ab11-4016-8e1e-090ba61d74dc",
            "prefLabel": {
                "nb": "avskiltingsdato"
            },
            "publisher": {
                "uri": "http://data.brreg.no/enhetsregisteret/enhet/974761076",
                "name": "SKATTEETATEN",
                "orgPath": "/STAT/972417807/974761076",
                "prefLabel": {
                    "no": "SKATTEETATEN"
                }
            }
        }
    ]
    result = group_by_org_uri(es_results=es_results)
    assert result.__len__() == 2


@pytest.mark.unit
def test_group_by_org_uri_should_discard_entries_without_empty_publisher():
    es_results = [
        {
            "id": "b970c1af-ab11-4016-8e1e-090ba61d74dc",
            "prefLabel": {
                "nb": "avskiltingsdato"
            },
            "publisher": {}
        },
        {
            "id": "b970c1af-ab11-4016-8e1e-090ba61d74dc",
            "prefLabel": {
                "nb": "avskiltingsdato"
            },
            "publisher": {
                "uri": "http://data.brreg.no/enhetsregisteret/enhet/974760673",
                "name": "REGISTERENHETEN I BRØNNØYSUND",
                "orgPath": "/STAT/912660680/974760673",
                "prefLabel": {
                    "no": "REGISTERENHETEN I BRØNNØYSUND"
                }
            }
        },
        {
            "id": "b970c1af-ab11-4016-8e1e-090ba61d74dc",
            "prefLabel": {
                "nb": "avskiltingsdato"
            },
            "publisher": {
                "uri": "http://data.brreg.no/enhetsregisteret/enhet/974761076",
                "name": "SKATTEETATEN",
                "orgPath": "/STAT/972417807/974761076",
                "prefLabel": {
                    "no": "SKATTEETATEN"
                }
            }
        },
        {
            "id": "b970c1af-ab11-4016-8e1e-090ba61d74dc",
            "prefLabel": {
                "nb": "avskiltingsdato"
            },
            "publisher": {
                "uri": "http://data.brreg.no/enhetsregisteret/enhet/974761076",
                "name": "SKATTEETATEN",
                "orgPath": "/STAT/972417807/974761076",
                "prefLabel": {
                    "no": "SKATTEETATEN"
                }
            }
        }
    ]
    result = group_by_org_uri(es_results=es_results)
    assert result.__len__() == 2


@pytest.mark.unit
def test_group_by_org_id():
    es_results = [
        {
            "id": "b970c1af-ab11-4016-8e1e-090ba61d74dc",
            "prefLabel": {
                "nb": "avskiltingsdato"
            },
            "publisher": {
                "id": "974760673",
                "name": "REGISTERENHETEN I BRØNNØYSUND",
                "orgPath": "/STAT/912660680/974760673",
                "prefLabel": {
                    "no": "REGISTERENHETEN I BRØNNØYSUND"
                }
            }
        },
        {
            "id": "b970c1af-ab11-4016-8e1e-090ba61d74dc",
            "prefLabel": {
                "nb": "avskiltingsdato"
            },
            "publisher": {
                "id": "974760673",
                "name": "REGISTERENHETEN I BRØNNØYSUND",
                "orgPath": "/STAT/912660680/974760673",
                "prefLabel": {
                    "no": "REGISTERENHETEN I BRØNNØYSUND"
                }
            }
        },
        {
            "id": "b970c1af-ab11-4016-8e1e-090ba61d74dc",
            "prefLabel": {
                "nb": "avskiltingsdato"
            },
            "publisher": {
                "id": "974761076",
                "name": "SKATTEETATEN",
                "orgPath": "/STAT/972417807/974761076",
                "prefLabel": {
                    "no": "SKATTEETATEN"
                }
            }
        }
    ]
    result = group_by_org_id(es_results=es_results)
    assert result.__len__() == 2


@pytest.mark.unit
def test_group_by_org_id_should_discard_entries_without_publisher():
    es_results = [
        {
            "id": "b970c1af-ab11-4016-8e1e-090ba61d74dc",
            "prefLabel": {
                "nb": "avskiltingsdato"
            }
        },
        {
            "id": "b970c1af-ab11-4016-8e1e-090ba61d74dc",
            "prefLabel": {
                "nb": "avskiltingsdato"
            },
            "publisher": {
                "id": "974760673",
                "name": "REGISTERENHETEN I BRØNNØYSUND",
                "orgPath": "/STAT/912660680/974760673",
                "prefLabel": {
                    "no": "REGISTERENHETEN I BRØNNØYSUND"
                }
            }
        },
        {
            "id": "b970c1af-ab11-4016-8e1e-090ba61d74dc",
            "prefLabel": {
                "nb": "avskiltingsdato"
            },
            "publisher": {
                "id": "974761076",
                "name": "SKATTEETATEN",
                "orgPath": "/STAT/972417807/974761076",
                "prefLabel": {
                    "no": "SKATTEETATEN"
                }
            }
        }
    ]
    result = group_by_org_id(es_results=es_results)
    assert result.__len__() == 2


@pytest.mark.unit
def test_group_by_org_id_should_discard_entries_without_empty_publisher():
    es_results = [
        {
            "id": "b970c1af-ab11-4016-8e1e-090ba61d74dc",
            "prefLabel": {
                "nb": "avskiltingsdato"
            },
            "publisher": {}
        },
        {
            "id": "b970c1af-ab11-4016-8e1e-090ba61d74dc",
            "prefLabel": {
                "nb": "avskiltingsdato"
            },
            "publisher": {
                "id": "974760673",
                "name": "REGISTERENHETEN I BRØNNØYSUND",
                "orgPath": "/STAT/912660680/974760673",
                "prefLabel": {
                    "no": "REGISTERENHETEN I BRØNNØYSUND"
                }
            }
        },
        {
            "id": "b970c1af-ab11-4016-8e1e-090ba61d74dc",
            "prefLabel": {
                "nb": "avskiltingsdato"
            },
            "publisher": {
                "id": "974761076",
                "name": "SKATTEETATEN",
                "orgPath": "/STAT/972417807/974761076",
                "prefLabel": {
                    "no": "SKATTEETATEN"
                }
            }
        }
    ]
    result = group_by_org_id(es_results=es_results)
    assert result.__len__() == 2


@pytest.mark.unit
def test_read_organization_rdf_xml():
    result = read_alt_organization_rdf_xml(geonorge_rdf_organization)
    assert result["orgPath"] == parsed_org_from_geonorge["orgPath"]


@pytest.mark.unit
def test_registry_checks():
    norwegian_registry = ParsedContent(name="Some Name",
                                       count=9,
                                       org_id="http://data.brreg.no/enhetsregisteret/enhet/974761076")
    alt_registry = ParsedContent(name="Some Name",
                                 count=9,
                                 org_id="http://otherregi-no.co/974761076")

    norwegian_registry_id = ParsedContent(name="Some Name",
                                          count=9,
                                          org_id="974761076")

    no_registry = ParsedContent(name="Some Name", count=88, org_id="some Name")

    assert norwegian_registry.get_norwegian_registry_id() == "974761076"
    assert alt_registry.get_norwegian_registry_id() is None
    assert norwegian_registry_id.get_norwegian_registry_id() == "974761076"
    assert no_registry.get_norwegian_registry_id() is None

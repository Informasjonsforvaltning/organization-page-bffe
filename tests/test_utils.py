import os

from src.utils import encode_for_sparql, sparql_queries, ServiceKey, \
    service_urls, get_service_urls


def test_encode_for_sparql():
    assert encode_for_sparql(string=sparql_queries[ServiceKey.DATASETS]) == expected_encoded_query


expected_encoded_query = "PREFIX%20dct:%20%3Chttp://purl.org/dc/terms/%3EPREFIX%20foaf:%20%3Chttp://xmlns.com/foaf/0.1/%3E" \
                         "%20PREFIX%20owl:%20%3Chttp://www.w3.org/2002/07/owl%23%3E%20SELECT%20?uri%20?name%20%28COUNT%28?item" \
                         "%29%20AS%20?count%29%20WHERE%20{" \
                         "%20?publisher%20a%20foaf:Agent%20.%20?item%20dct:publisher%20?publisher%20.%20{" \
                         "%20SELECT%20?publisher%20?uri%20?name%20WHERE%20{%20?publisher%20a%20foaf:Agent%20.%20OPTIONAL%20{" \
                         "%20?publisher%20foaf:name%20?name%20.%20}%20OPTIONAL%20{" \
                         "%20?publisher%20owl:sameAs%20?sameAs%20.%20}%20BIND%28COALESCE%28?sameAs," \
                         "%20STR%28?publisher%29%29%20AS%20?uri%29%20}%20}%20}%20GROUP%20BY%20?uri%20?name%20ORDER%20BY%20DESC" \
                         "%28?count%29"


def test_get_service_urls(monkeypatch):
    assert service_urls[ServiceKey.ORGANIZATIONS] == "http://localhost:8080/organizations"
    monkeypatch.setenv('ORGANIZATION_CATALOG_URL', 'http://testenv:8080')
    assert get_service_urls(ServiceKey.ORGANIZATIONS) == "http://testenv:8080/organizations"

    assert service_urls[ServiceKey.INFO_MODELS] == "http://localhost:8080/informationmodels"
    monkeypatch.setenv("INFORMATIONMODELS_HARVESTER_URL", "http://othertestenv:8080")
    assert get_service_urls(ServiceKey.INFO_MODELS) == "http://othertestenv:8080/informationmodels"

    assert service_urls[ServiceKey.DATASETS] == "http://localhost:8080"
    monkeypatch.setenv("DATASET_HARVESTER_URL", "http://othertestenv:8080")
    assert get_service_urls(ServiceKey.DATASETS) == "http://othertestenv:8080"

    assert service_urls[ServiceKey.CONCEPTS] == "http://localhost:8080/concepts"
    monkeypatch.setenv("CONCEPT_HARVESTER_URL", "http://something.yes")
    assert get_service_urls(ServiceKey.CONCEPTS) == "http://something.yes/concepts"

    assert service_urls[ServiceKey.DATA_SERVICES] == "http://localhost:8080/apis"
    monkeypatch.setenv("DATASERVICE_HARVESTER_URL", "http://testenv:8080")
    assert get_service_urls(ServiceKey.DATA_SERVICES) == "http://testenv:8080/apis"

import pytest
import requests

service_url = "http://localhost:8000"
org_catalog_url = f"{service_url}/organizationcatalogs"
# update if change in mockdata
expected_size = 22


class TestSearchAll:

    @pytest.mark.contract
    def test_has_correct_format(self, wait_for_ready):
        result = requests.get(url=org_catalog_url, timeout=10)
        assert result.status_code == 200
        assert len(result.json()["organizations"]) == expected_size
        for org in result.json()["organizations"]:
            keys = org.keys()
            assert "id" in keys
            assert "organization" in keys
            assert "dataset_count" in keys
            assert "concept_count" in keys
            assert "informationmodel_count" in keys
            assert "dataservice_count" in keys
            organization = org["organization"]
            org_keys = organization.keys()
            assert "name" in org_keys
            assert is_language_object_with_content(organization["name"]), "Error: found organization without name: {0}" \
                .format(organization)
            assert "orgPath" in org_keys

    @pytest.mark.contract
    def test_brreg_has_correct_data(self, wait_for_ready):
        result = requests.get(url=org_catalog_url, timeout=10)
        if result.status_code != 200:
            pytest.xfail(f"Response status code was{result.status_code}")
        else:
            for org in result.json()["organizations"]:
                if org["id"] == "974760673":
                    assert org["dataset_count"] == 643
                    assert org["informationmodel_count"] == 0
                    assert org["concept_count"] == 7
                    assert org["dataservice_count"] == 3

    @pytest.mark.contract
    def test_brreg_has_correct_dataset_counts(self, wait_for_ready):
        result = requests.get(url=org_catalog_url, timeout=10)
        if result.status_code != 200:
            pytest.xfail(f"Response status code was{result.status_code}")
        else:
            for org in result.json()["organizations"]:
                if org["id"] == "971040238":
                    assert org["dataset_count"] == 109
                if org["id"] == "https://prod.nora.links.com.au/organization/e6d3dc7a-752e-418b-9afd-36533b370285":
                    assert org["dataset_count"] == 49
                if org["id"] == "971032081":
                    assert org["dataset_count"] == 5

    @pytest.mark.contract
    def test_has_correct_informationmodel_counts(self, wait_for_ready):
        result = requests.get(url=org_catalog_url, timeout=10)
        if result.status_code != 200:
            pytest.xfail(f"Response status code was{result.status_code}")
        else:
            for org in result.json()["organizations"]:
                if org["id"] == "971040238":  # Kartverket
                    assert org["informationmodel_count"] == 0
                if org[
                    "id"] == "https://prod.nora.links.com.au/organization/e6d3dc7a-752e-418b-9afd-36533b370285":  # SV, bad uri
                    assert org["informationmodel_count"] == 0
                if org["id"] == "974761076":  # Skatteetaten
                    assert org["informationmodel_count"] == 3
                if org["id"] == "971203420":  # Fiskeridepartementet
                    assert org["informationmodel_count"] == 1

    @pytest.mark.contract
    def test_has_correct_concept_counts(self, wait_for_ready):
        result = requests.get(url=org_catalog_url, timeout=10)
        if result.status_code != 200:
            pytest.xfail(f"Response status code was{result.status_code}")
        else:
            for org in result.json()["organizations"]:
                if org["id"] == "971040238":  # Kartverket
                    assert org["concept_count"] == 0
                if org[
                    "id"] == "https://prod.nora.links.com.au/organization/e6d3dc7a-752e-418b-9afd-36533b370285":  # SV, bad uri
                    assert org["concept_count"] == 0
                if org["id"] == "971526157":  # Patentstyret:
                    assert org["concept_count"] == 3

    @pytest.mark.contract
    def test_has_correct_dataservice_counts(self, wait_for_ready):
        result = requests.get(url=org_catalog_url, timeout=10)
        if result.status_code != 200:
            pytest.xfail(f"Response status code was{result.status_code}")
        else:
            for org in result.json()["organizations"]:
                if org["id"] == "971040238":  # Kartverket
                    assert org["dataservice_count"] == 3
                if org[
                    "id"] == "https://prod.nora.links.com.au/organization/e6d3dc7a-752e-418b-9afd-36533b370285":  # SV, bad uri
                    assert org["dataservice_count"] == 0
                if org["id"] == "974761076":  # Skatteetaten
                    assert org["dataservice_count"] == 1
                if org["id"] == "971203420":  # Fiskeridepartementet
                    assert org["dataservice_count"] == 0


def is_language_object_with_content(entry: dict):
    keys = entry.keys()
    return ("nn" in keys and entry["nn"] != "") \
           or ("nb" in keys and entry["nb"] != "") \
           or ("en" in keys and entry["en"] != "") \
           or ("no" in keys and entry["no"] != "")

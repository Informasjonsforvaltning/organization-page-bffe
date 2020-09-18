import pytest
import requests

service_url = "http://localhost:8000"
org_catalog_url = f"{service_url}/organizationcatalogs"
# update if change in mockdata
expected_size = 13


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
            org_path: str = organization["orgPath"]
            assert org_path is not None, "Error: entry with missing org"
            assert org_path.startswith("/"), f"Error: {org_path} is not a valid orgPath"

    @pytest.mark.contract
    def test_brreg_has_correct_data(self, wait_for_ready):
        result = requests.get(url=org_catalog_url, timeout=10)
        if result.status_code != 200:
            pytest.xfail(f"Response status code was{result.status_code}")
        else:
            for org in result.json()["organizations"]:
                if org["id"] == "974760673":
                    assert org["dataset_count"] == 3
                    assert org["informationmodel_count"] == 25
                    assert org["concept_count"] == 32
                    assert org["dataservice_count"] == 0

    @pytest.mark.contract
    def test_brreg_has_correct_dataset_counts(self, wait_for_ready):
        result = requests.get(url=org_catalog_url, timeout=10)
        if result.status_code != 200:
            pytest.xfail(f"Response status code was{result.status_code}")
        else:
            for org in result.json()["organizations"]:
                if org["id"] == "994686011":
                    assert org["dataset_count"] == 2
                if org["id"] == "983544622":
                    assert org["dataset_count"] == 6
                if org["id"] == "867668292":
                    assert org["dataset_count"] == 1
                if org["id"] == "971032081":
                    assert org["dataset_count"] == 59

    @pytest.mark.contract
    def test_has_correct_informationmodel_counts(self, wait_for_ready):
        result = requests.get(url=org_catalog_url, timeout=10)
        if result.status_code != 200:
            pytest.xfail(f"Response status code was{result.status_code}")
        else:
            for org in result.json()["organizations"]:
                if "id" in org.keys():
                    if org["id"] == "994686011":
                        assert org["informationmodel_count"] == 0
                    if org["id"] == "974761076":
                        assert org["informationmodel_count"] == 90

    @pytest.mark.contract
    def test_has_correct_concept_counts(self, wait_for_ready):
        result = requests.get(url=org_catalog_url, timeout=10)
        if result.status_code != 200:
            pytest.xfail(f"Response status code was{result.status_code}")
        else:
            for org in result.json()["organizations"]:
                if "id" in org.keys():
                    if org["id"] == "840747972":
                        assert org["concept_count"] == 44
                    if org["id"] == "974761262":
                        assert org["concept_count"] == 20

    @pytest.mark.contract
    def test_has_correct_dataservice_counts(self, wait_for_ready):
        result = requests.get(url=org_catalog_url, timeout=10)
        if result.status_code != 200:
            pytest.xfail(f"Response status code was{result.status_code}")
        else:
            has_dataservice_count_higher_than_zero = False
            for org in result.json()["organizations"]:
                if org["dataservice_count"] > 0:
                    has_dataservice_count_higher_than_zero = True
                if org["id"] == "910258028":
                    assert org["dataservice_count"] == 17
                if org["id"] == "910244132":
                    assert org["dataservice_count"] == 20
            assert has_dataservice_count_higher_than_zero


def is_language_object_with_content(entry: dict):
    keys = entry.keys()
    return ("nn" in keys and entry["nn"] != "") \
           or ("nb" in keys and entry["nb"] != "") \
           or ("en" in keys and entry["en"] != "") \
           or ("no" in keys and entry["no"] != "")

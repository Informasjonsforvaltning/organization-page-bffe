from unittest.mock import MagicMock

import pytest
from src.aggregation import get_organization_catalog_list
from src.utils import FetchFromServiceException
from src.service_requests import ServiceKey
from tests.test_data import org_1, org_2, org_3, concept_response, dataset_response, dataservice_response, \
    info_model_response, org_5


@pytest.fixture
def mock_get_organizations(mocker):
    return mocker.patch('src.aggregation.get_organizations',
                        return_value=[org_1, org_2, org_3, org_5]
                        )


@pytest.fixture
def mock_get_organizations_exception(mocker):
    return mocker.patch('src.aggregation.get_organizations',
                        side_effect=FetchFromServiceException(
                            execution_point=ServiceKey.ORGANIZATIONS,
                            url="http://mock.grape/organizations"
                        ))


@pytest.fixture
def mock_get_concepts(mocker):
    return mocker.patch('src.aggregation.get_concepts_for_organization', return_value=concept_response(92))


@pytest.fixture
def mock_get_concepts_exception(mocker):
    return mocker.patch('src.aggregation.get_concepts_for_organization', side_effect=FetchFromServiceException(
        execution_point=ServiceKey.CONCEPTS,
        url="http://mock.grape/concepts"
    ))


@pytest.fixture
def mock_get_datasets(mocker):
    return mocker.patch('src.aggregation.get_datasets_for_organization', return_value=dataset_response(8))


@pytest.fixture
def mock_get_datasets_exception(mocker):
    return mocker.patch('src.aggregation.get_datasets_for_organization', side_effect=FetchFromServiceException(
        execution_point=ServiceKey.DATA_SETS,
        url="http://mock.grape/dataset"
    ))


@pytest.fixture
def mock_get_dataservices(mocker):
    return mocker.patch('src.aggregation.get_dataservices_for_organization', return_value=dataservice_response(23))


@pytest.fixture
def mock_get_dataservices_exception(mocker):
    return mocker.patch('src.aggregation.get_dataservices_for_organization', side_effect=FetchFromServiceException(
        execution_point=ServiceKey.DATA_SERVICES,
        url="http://mock.grape/dataservices"
    ))


@pytest.fixture()
def mock_get_informationmodels(mocker):
    return mocker.patch('src.aggregation.get_informationmodels_for_organization',
                        return_value=info_model_response(1))


@pytest.fixture()
def mock_get_informationmodels_exception(mocker):
    return mocker.patch('src.aggregation.get_informationmodels_for_organization', side_effect=FetchFromServiceException(
        execution_point=ServiceKey.INFO_MODELS,
        url="http://mock.grape/informationmodels"
    ))


@pytest.mark.unit
def test_get_organization_catalog_list(mock_get_organizations,
                                       mock_get_concepts,
                                       mock_get_datasets,
                                       mock_get_dataservices,
                                       mock_get_informationmodels):
    orgpath_list = [org_1["orgPath"], org_2["orgPath"], org_3["orgPath"], org_5["orgPath"]]
    result = get_organization_catalog_list()
    assert mock_get_organizations.call_count == 1
    assert mock_get_concepts.call_count == 4
    assert mock_get_informationmodels.call_count == 4
    assert mock_get_datasets.call_count == 4
    assert mock_get_dataservices.call_count == 4
    assert called_with_all_orgPaths(mock_get_concepts, orgpath_list)
    assert called_with_all_orgPaths(mock_get_informationmodels, orgpath_list)
    assert called_with_all_orgPaths(mock_get_dataservices, orgpath_list)
    assert called_with_all_orgPaths(mock_get_datasets, orgpath_list)
    assert result.org_list.__len__() == 4


@pytest.mark.unit
def test_get_organization_catalog_should_return_error_msg_for_organizations(mock_get_organizations_exception,
                                                                            mock_get_concepts,
                                                                            mock_get_datasets,
                                                                            mock_get_informationmodels,
                                                                            mock_get_dataservices):
    result = get_organization_catalog_list()
    assert "status" in result.keys()
    assert result["status"] == "error"
    assert "reason" in result.keys()
    assert "organization" in result["reason"]


@pytest.mark.unit
def test_get_organization_catalog_should_return_error_msg_for_concepts(mock_get_organizations,
                                                                       mock_get_concepts_exception,
                                                                       mock_get_datasets,
                                                                       mock_get_informationmodels,
                                                                       mock_get_dataservices):
    result = get_organization_catalog_list()
    assert "status" in result.keys()
    assert result["status"] == "error"
    assert "reason" in result.keys()
    assert "concepts" in result["reason"]


@pytest.mark.unit
def test_get_organization_catalog_should_return_error_msg_for_datasets(mock_get_organizations,
                                                                       mock_get_concepts,
                                                                       mock_get_datasets_exception,
                                                                       mock_get_informationmodels,
                                                                       mock_get_dataservices):
    result = get_organization_catalog_list()
    assert "status" in result.keys()
    assert result["status"] == "error"
    assert "reason" in result.keys()
    assert "datasets" in result["reason"]


@pytest.mark.unit
def test_get_organization_catalog_should_return_error_msg_for_dataservices(mock_get_organizations,
                                                                           mock_get_concepts,
                                                                           mock_get_datasets,
                                                                           mock_get_informationmodels,
                                                                           mock_get_dataservices_exception):
    result = get_organization_catalog_list()
    assert "status" in result.keys()
    assert result["status"] == "error"
    assert "reason" in result.keys()
    assert "dataservices" in result["reason"]


@pytest.mark.unit
def test_get_organization_catalog_should_return_error_msg_for_informationmodels(mock_get_organizations,
                                                                           mock_get_concepts,
                                                                           mock_get_datasets,
                                                                           mock_get_informationmodels_exception,
                                                                           mock_get_dataservices):
    result = get_organization_catalog_list()
    assert "status" in result.keys()
    assert result["status"] == "error"
    assert "reason" in result.keys()
    assert "informationmodels" in result["reason"]


def called_with_all_orgPaths(mock: MagicMock, org_path_list: list):
    args = []
    for call in mock.call_args_list:
        args.append(call[0][0])

    all_orgpaths = set(args).union(set(org_path_list))
    return all_orgpaths.__len__() == args.__len__()

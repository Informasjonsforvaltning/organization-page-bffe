from src.responses import OrganizationCatalogResponse, OrganizationCatalogListResponse
from src.service_requests import get_organizations, get_datasets_for_organization, get_dataservices_for_organization, \
    get_concepts_for_organization, get_informationmodels_for_organization
from src.utils import FetchFromServiceException


def get_organization_catalog_list():
    response_list = OrganizationCatalogListResponse()
    try:
        organizations = get_organizations()
        for organization in organizations:
            # temporary fix for discrepancies between orgpaths in organization catalog and harvester
            old_format = get_old_org_path_format(organization["orgPath"])
            organization["orgPath"] = old_format
            catalog = OrganizationCatalogResponse(
                organization=organization,
                datasets=get_datasets_for_organization(old_format),
                dataservices=get_dataservices_for_organization(old_format),
                concepts=get_concepts_for_organization(old_format),
                informationmodels=get_informationmodels_for_organization(old_format)
            )
            response_list.add_organization_catalog(catalog)
        return response_list
    except FetchFromServiceException as err:
        return err.__dict__


def get_old_org_path_format(org_path: str):
    if org_path.startswith("/"):
        return org_path
    else:
        return f"/{org_path}"

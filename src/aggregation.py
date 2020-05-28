import asyncio

from src.responses import OrganizationCatalogResponse, OrganizationCatalogListResponse
from src.service_requests import get_organizations, get_concepts_for_organization, get_dataservices_for_organization, \
    get_datasets_for_organization, get_informationmodels_for_organization
from src.utils import FetchFromServiceException


def get_organization_catalog_list():
    response_list = OrganizationCatalogListResponse()
    try:
        organizations = get_organizations()
        for organization in organizations:
            # temporary fix for discrepancies between orgpaths in organization catalog and harvester
            old_format = get_old_org_path_format(organization["orgPath"])
            organization["orgPath"] = old_format
            catalog = get_catalog_for_organization(organization)
            response_list.add_organization_catalog(catalog)
            print(f"fetching catalog for {organization}")
        return response_list
    except FetchFromServiceException as err:
        return err.__dict__


def get_catalog_for_organization(organization):
    old_format = get_old_org_path_format(organization["orgPath"])
    new_format = get_new_org_path_format(organization["orgPath"])
    organization["orgPath"] = old_format
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    content_requests = asyncio.gather(get_concepts_for_organization(old_format),
                                      get_datasets_for_organization(old_format),
                                      get_dataservices_for_organization(old_format),
                                      get_informationmodels_for_organization(new_format)
                                      )
    concepts, datasets, dataservices, informationmodels = loop.run_until_complete(content_requests)
    loop.close()
    return OrganizationCatalogResponse(
        organization=organization,
        concepts=concepts,
        informationmodels=informationmodels,
        datasets=datasets,
        dataservices=dataservices
    )


def get_old_org_path_format(org_path: str):
    if org_path.startswith("/"):
        return org_path
    else:
        return f"/{org_path}"


def get_new_org_path_format(orgPath: str):
    if orgPath.startswith("/"):
        return orgPath[1:]
    else:
        return orgPath

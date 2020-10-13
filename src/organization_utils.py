from src.service_requests import fetch_organization_by_id, fetch_generated_org_path_from_organization_catalog
from src.utils import OrganizationCatalogResult, NotInNationalRegistryException, FetchFromServiceException


async def get_organization(org_id: str) -> OrganizationCatalogResult:
    try:
        return await fetch_organization_by_id(org_id)
    except (NotInNationalRegistryException, FetchFromServiceException):
        return OrganizationCatalogResult(org_id=org_id)


async def get_generated_org_path(name) -> str:
    if name is not None:
        return await fetch_generated_org_path_from_organization_catalog(name=name)
    else:
        return None

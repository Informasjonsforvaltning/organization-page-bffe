import asyncio

from src.service_requests import fetch_organization_by_id, fetch_generated_org_path_from_organization_catalog
from src.utils import OrganizationCatalogResult, NotInNationalRegistryException


async def get_organization(org_id, name) -> OrganizationCatalogResult:
    if org_id is not None or name is not None:
        try:
            return await fetch_organization_by_id(org_id, name)
        except NotInNationalRegistryException:
            org_path = get_generated_org_path(name)
            return OrganizationCatalogResult(
                org_path=await org_path
            )
    else:
        return None


async def get_generated_org_path(name) -> str:
    if name is not None:
        return await fetch_generated_org_path_from_organization_catalog(name=name)
    else:
        return None

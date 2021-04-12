"""Resource module for specific organization catalog."""
from dataclasses import asdict

from aiohttp.web import json_response, Response, View

from fdk_organization_bff.service.org_catalog_service import get_organization_catalogs


class OrgCatalogs(View):
    """Class representing organization catalogs resource."""

    async def get(self: View) -> Response:
        """Get all organization catalogs."""
        catalogs = await get_organization_catalogs()
        return json_response(asdict(catalogs))

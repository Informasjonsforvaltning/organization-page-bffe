"""Resource module for specific organization catalog."""
from dataclasses import asdict

from aiohttp.web import json_response, Response, View

from fdk_organization_bff.service.org_catalog_service import get_organization_catalog


class OrgCatalog(View):
    """Class representing organization catalog resource."""

    async def get(self: View) -> Response:
        """Get specific organization catalog."""
        catalog = await get_organization_catalog(self.request.match_info["id"])
        if catalog:
            return json_response(asdict(catalog))
        else:
            return Response(status=404)

"""Resource module for specific organization catalog."""
from dataclasses import asdict

from aiohttp.web import json_response, Response, View

from fdk_organization_bff.classes import FilterEnum
from fdk_organization_bff.service.org_catalog_service import get_organization_catalogs
from fdk_organization_bff.utils.utils import filter_param_to_enum


class OrgCatalogs(View):
    """Class representing organization catalogs resource."""

    async def get(self: View) -> Response:
        """Get all organization catalogs."""
        filter = filter_param_to_enum(self.request.rel_url.query.get("filter"))
        if filter is FilterEnum.INVALID:
            return Response(status=400)
        else:
            catalogs = await get_organization_catalogs(filter)
            return json_response(asdict(catalogs))

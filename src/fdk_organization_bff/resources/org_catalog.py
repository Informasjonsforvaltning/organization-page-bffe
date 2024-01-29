"""Resource module for specific organization catalog."""

from dataclasses import asdict

from aiohttp.web import json_response, Response, View

from fdk_organization_bff.classes import FilterEnum
from fdk_organization_bff.service.org_catalog_service import get_organization_catalog
from fdk_organization_bff.utils.utils import filter_param_to_enum
from .utils import fifteen_min_cache_header


class OrgCatalog(View):
    """Class representing organization catalog resource."""

    async def get(self: View) -> Response:
        """Get specific organization catalog."""
        filter = filter_param_to_enum(self.request.rel_url.query.get("filter"))
        if filter is FilterEnum.INVALID:
            return Response(status=400)
        else:
            catalog = await get_organization_catalog(
                self.request.match_info["id"], filter
            )
            if catalog:
                return json_response(asdict(catalog), headers=fifteen_min_cache_header)
            else:
                return Response(status=404)

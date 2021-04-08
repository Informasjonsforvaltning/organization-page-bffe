"""Module for starting an aiohttp API."""
import logging

from aiohttp import web

from fdk_organization_bff.config import Config
from fdk_organization_bff.resources import OrgCatalog, Ping, Ready


def setup_routes(app: web.Application) -> None:
    """Add active routes to application."""
    app.add_routes(
        [
            web.get(Config.routes()["PING"], Ping),
            web.get(Config.routes()["READY"], Ready),
            web.get(Config.routes()["ORG_CATALOG"], OrgCatalog),
        ]
    )


async def create_app() -> web.Application:
    """Create aiohttp application."""
    app = web.Application()
    logging.basicConfig(level=logging.INFO)
    setup_routes(app)
    return app

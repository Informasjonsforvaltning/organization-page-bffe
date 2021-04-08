"""Resource module for ready."""
from aiohttp.web import Response, View


class Ready(View):
    """Class representing ready resource."""

    @staticmethod
    async def get() -> Response:
        """Ready route function."""
        return Response(text="OK")

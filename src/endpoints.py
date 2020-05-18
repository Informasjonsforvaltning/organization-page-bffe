from flask_restful import Resource, abort

from src.service_requests import is_ready


class OrganizationCatalogs(Resource):
    def get(self):
        abort(http_status_code=501, description="Not implemented")


class OrganizationCatalogWithId(Resource):
    def get(self, organization_id: str):
        print(organization_id)
        abort(http_status_code=501, description="Not implemented")


class Ready(Resource):
    def get(self):
        result = is_ready()
        if result["status"] == "error":
            abort(http_status_code=503, description=result["reason"])
        else:
            return result

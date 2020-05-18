from flask_restful import Resource, abort


class OrganizationCatalogs(Resource):
    def get(self):
        abort(http_status_code=501, description="Not implemented")


class OrganizationCatalogWithId(Resource):
    def get(self, organization_id: str):
        print(organization_id)
        abort(http_status_code=501, description="Not implemented")

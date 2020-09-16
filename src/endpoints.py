import asyncio
from flask import request
from flask_restful import Resource, abort

from src.aggregation import get_organization_catalog_list
from src.service_requests import (
    get_assessments_for_entities,
    get_assessment_for_entity,
    get_catalog_assessment_rating_for_entity_type,
    get_organization_from_organization_catalogue,
    search_datasets
)


class OrganizationCatalogs(Resource):
    def get(self):
        result = get_organization_catalog_list()
        if isinstance(result, dict):
            abort(http_status_code=500, description=result["reason"])
        else:
            return result.map_response()


class OrganizationCatalogWithId(Resource):
    def get(self, organization_id: str):
        print(organization_id)
        abort(http_status_code=501, description="Not implemented")


class DatasetCatalogForOrganization(Resource):
    def get(self, organization_id: str):
        page = request.args.get("page", default=0, type=int)
        size = request.args.get("size", default=10, type=int)

        try:
            organization = asyncio.run(get_organization_from_organization_catalogue(organization_id))

            paged_datasets = asyncio.run(search_datasets({
                "filters": [
                    {
                        "orgPath": organization["orgPath"]
                    }
                ],
                "page": page,
                "size": size
            }))

            entity_uris = list(map(lambda hit: hit["uri"], paged_datasets["hits"]))

            if entity_uris:
                assessments = asyncio.run(get_assessments_for_entities(entity_uris))

                paged_datasets["hits"] = list(map(lambda hit: {
                    **hit,
                    # INFO: find first assessment by id or return None
                    "assessment": next((assessment for assessment in assessments if assessment["id"] == hit["uri"]),
                                       None)
                }, paged_datasets["hits"]))

            try:
                catalog_uri = paged_datasets["hits"][0]["catalog"]["uri"]
            except AttributeError:
                catalog_uri = None

            if catalog_uri:
                assessment_rating = asyncio.run(get_catalog_assessment_rating_for_entity_type(catalog_uri, "dataset"))

            return {
                **paged_datasets,
                "rating": assessment_rating
            }
        except Exception as e:
            abort(http_status_code=500, description=str(e))


class DatasetForOrganization(Resource):
    def get(self, organization_id: str, dataset_id: str):
        try:
            datasets = asyncio.run(search_datasets({
                "filters": [
                    {
                        "_id": dataset_id
                    }
                ]
            }))

            try:
                dataset = datasets["hits"][0]
            except AttributeError:
                abort(http_status_code=404, description=f"Could not find dataset with ID: {dataset_id}")

            assessment = asyncio.run(get_assessment_for_entity(dataset["uri"]))

            return {
                "datset": dataset,
                "assessment": assessment
            }
        except Exception as e:
            abort(http_status_code=500, description=str(e))


class Ping(Resource):
    def get(self):
        return 200


class Ready(Resource):
    def get(self):
        return "service is running"

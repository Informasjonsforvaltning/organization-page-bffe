def get_name(organization):
    org_keys = organization.keys()
    if "prefLabel" in org_keys and organization["prefLabel"] is not None:
        return organization["prefLabel"]
    else:
        return {
            "no": organization["name"]
        }


class OrganizationCatalogResponse:
    def __init__(self, organization, datasets, dataservices, concepts, informationmodels):
        self.id = organization["organizationId"]
        self.organization = {
            "orgPath": organization["orgPath"],
            "name": get_name(organization),
        }
        self.dataset_count = datasets["hits"]["total"]
        self.dataservice_count = dataservices["total"]
        self.informationmodel_count = informationmodels["page"]["totalElements"]
        self.concept_count = concepts["page"]["totalElements"]


class OrganizationCatalogListResponse:
    def __init__(self):
        self.org_list = []

    def add_organization_catalog(self, organization_catalog: OrganizationCatalogResponse):
        self.org_list.append(organization_catalog.__dict__)

    def map_response(self):
        return {
            "organizations": self.org_list
        }

    def keys(self):
        return {
            "status": "OK"
        }

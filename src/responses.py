from src.result_readers import OrganizationReferencesObject


def get_name(organization):
    org_keys = organization.keys()
    if "prefLabel" in org_keys and organization["prefLabel"] is not None:
        return organization["prefLabel"]
    else:
        return {
            "no": organization["name"]
        }


class OrganizationCatalogResponse:
    def __init__(self, organization: dict, datasets: OrganizationReferencesObject, dataservices: OrganizationReferencesObject,
                 concepts: OrganizationReferencesObject, informationmodels: OrganizationReferencesObject):
        if "organizationId" in organization.keys():
            self.id = organization["organizationId"]
        self.organization = {
            "orgPath": organization["orgPath"],
            "name": get_name(organization),
        }
        self.dataset_count = datasets.count if datasets else 0
        self.dataservice_count = dataservices.count if dataservices else 0
        self.informationmodel_count = informationmodels.count if informationmodels else 0
        self.concept_count = concepts.count if concepts else 0

    def has_content(self):
        return self.dataservice_count + self.informationmodel_count + self.dataset_count + self.concept_count > 0


class OrganizationCatalogListResponse:
    def __init__(self):
        self.org_list = []

    def add_organization_catalog(self, organization_catalog: OrganizationCatalogResponse):
        if organization_catalog.has_content():
            self.org_list.append(organization_catalog.__dict__)

    def map_response(self):
        return {
            "organizations": self.org_list
        }

    def count(self):
        return len(self.org_list)

    def keys(self):
        return {
            "status": "OK"
        }

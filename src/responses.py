from src.result_readers import OrganizationReferencesObject, OrganizationStore
from src.utils import ContentKeys


def get_name(organization: OrganizationReferencesObject) -> dict:
    # TODO: add support for several languages

    return {
        "no": organization.name
    }


class OrganizationCatalogResponse:
    def __init__(self, organization: OrganizationReferencesObject):
        self.organization = {
            ContentKeys.ORG_PATH: organization.org_path,
            ContentKeys.ORG_NAME: get_name(organization),
        }
        self.dataset_count = organization.dataset_count
        self.dataservice_count = organization.dataservice_count
        self.informationmodel_count = organization.informationmodel_count
        self.concept_count = organization.concept_count
        self.id = organization.resolve_display_id()

    def has_content(self):
        return self.dataservice_count + self.informationmodel_count + self.dataset_count + self.concept_count > 0


class OrganizationCatalogListResponse:
    def __init__(self):
        self.org_list = []

    def add_organization_catalog(self, organization_catalog: OrganizationCatalogResponse):
        if organization_catalog.has_content() and organization_catalog.id:
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

    @staticmethod
    def from_organization_store(organization_store: OrganizationStore) -> 'OrganizationCatalogListResponse':
        list_response = OrganizationCatalogListResponse()
        for org_ref in organization_store.get_organization_list():
            list_response.add_organization_catalog(
                OrganizationCatalogResponse(org_ref)
            )
        return list_response

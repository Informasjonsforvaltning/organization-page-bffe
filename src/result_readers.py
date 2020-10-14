import re
from typing import List, Iterable

from src.organization_utils import get_organization
from src.utils import ContentKeys, OrgCatalogKeys, ServiceKey, OrganizationCatalogResult

NATIONAL_REGISTRY_PATTERN = "data.brreg.no/enhetsregisteret"
NATIONAL_REGISTRY_URL = "https://data.brreg.no/enhetsregisteret/api/enheter"
ORGANIZATION_CATALOG_IDENTIFIER_PATTERN = "organization-catalog.[a-z.]*fellesdatakatalog"


class OrganizationReferencesObject:

    def __init__(self,
                 for_service: ServiceKey,
                 org_id: str = None,
                 org_uri: str = None,
                 org_path: str = None,
                 same_as_entry: str = None,
                 name: str = None,
                 count: int = 0):
        self.org_uri: str = org_uri
        self.org_path: str = org_path
        self.same_as: List[str] = []
        if same_as_entry:
            self.same_as.append(same_as_entry)
        self.name: str = name
        self.dataset_count = count if for_service == ServiceKey.DATASETS else 0
        self.dataservice_count = count if for_service == ServiceKey.DATA_SERVICES else 0
        self.concept_count = count if for_service == ServiceKey.CONCEPTS else 0
        self.informationmodel_count = count if for_service == ServiceKey.INFO_MODELS else 0
        self.id = org_id if org_id else self.get_org_id_from_org_path()

    def set_count_value(self, for_service: ServiceKey, count):
        if for_service == ServiceKey.DATASETS:
            self.dataset_count = int(count)
        elif for_service == ServiceKey.DATA_SERVICES:
            self.dataservice_count = int(count)
        elif for_service == ServiceKey.INFO_MODELS:
            self.informationmodel_count = count
        elif for_service == ServiceKey.CONCEPTS:
            self.concept_count = count

    def get_count_value(self, for_service: ServiceKey) -> int:
        if for_service == ServiceKey.DATASETS:
            return self.dataset_count
        elif for_service == ServiceKey.DATA_SERVICES:
            return self.dataservice_count
        elif for_service == ServiceKey.INFO_MODELS:
            return self.informationmodel_count
        elif for_service == ServiceKey.CONCEPTS:
            return self.concept_count
        else:
            return 0

    def __eq__(self, other):
        return type(other) == OrganizationReferencesObject and self.id == other.id

    def __hash__(self):
        return hash((
            self.org_uri,
            self.org_path,
            self.same_as,
            self.name,
            self.dataset_count,
            self.dataservice_count,
            self.concept_count,
            self.informationmodel_count,
            self.id
        ))

    @staticmethod
    def from_organization_catalog_single_response(organization: dict):
        return OrganizationReferencesObject(
            org_id=organization[OrgCatalogKeys.ID],
            for_service=ServiceKey.ORGANIZATIONS,
            org_uri=organization[OrgCatalogKeys.URI],
            org_path=organization[OrgCatalogKeys.ORG_PATH],
            name=organization[OrgCatalogKeys.NAME]
        )

    @staticmethod
    def from_organization_catalog_list_response(organizations: Iterable):
        return [OrganizationReferencesObject.from_organization_catalog_single_response(org) for org in organizations]

    @staticmethod
    def from_sparql_query_result(for_service: ServiceKey, organization: dict) -> 'OrganizationReferencesObject':
        try:
            id = organization.get(ContentKeys.ORGANIZATION_NUMBER).get(ContentKeys.VALUE)
        except AttributeError:
            id = None

        return OrganizationReferencesObject(
            for_service=for_service,
            org_id=id.strip(),
            count=int(organization.get(ContentKeys.COUNT).get(ContentKeys.VALUE))
        )

    @staticmethod
    def from_sparql_bindings(for_service: ServiceKey, sparql_bindings: Iterable):
        return [OrganizationReferencesObject.from_sparql_query_result(
            for_service=for_service,
            organization=binding
        ) for binding in sparql_bindings]

    @staticmethod
    def from_es_bucket(for_service: ServiceKey, es_bucket: dict):
        return OrganizationReferencesObject(
            for_service=for_service,
            org_path=es_bucket[ContentKeys.KEY],
            count=es_bucket[ContentKeys.COUNT]
        )

    @staticmethod
    def from_es_response_list(for_service, es_response: List[dict]) -> List['OrganizationReferencesObject']:
        return [
            OrganizationReferencesObject.from_es_bucket(for_service, bucket)
            for bucket in es_response[ContentKeys.AGGREGATIONS][ContentKeys.ORG_PATH][ContentKeys.BUCKETS]
        ]

    def get_org_id_from_org_path(self):
        return self.org_path.split("/").pop() if self.org_path else None

    def update_with_catalog_entry(self, entry: OrganizationCatalogResult):
        self.name = entry.name or self.name
        self.id = entry.org_id or self.id
        self.org_path = entry.org_path

    def clear_count_values(self):
        self.dataset_count = 0
        self.dataservice_count = 0
        self.concept_count = 0
        self.informationmodel_count = 0


class OrgPathParent:
    def __init__(self, org_path: str):
        if org_path:
            self.org_path_joints = org_path.split("/")

    def __eq__(self, other: 'OrgPathParent'):
        try:
            if len(other.org_path_joints) > len(self.org_path_joints):
                for idx, joint in enumerate(self.org_path_joints):
                    if other.org_path_joints[idx] != joint:
                        return False
                return True
            return False
        except AttributeError:
            return False


class OrganizationStore:
    __instance__: 'OrganizationStore' = None

    def __init__(self):
        if OrganizationStore.__instance__ is None:
            self.organizations: List[OrganizationReferencesObject] = None
            self.org_path_parents: List[OrgPathParent] = None
            OrganizationStore.__instance__ = self
        else:
            raise OrganizationStoreExistsException()

    def get_organization_list(self) -> List[OrganizationReferencesObject]:
        return [org for org in self.organizations
                if OrgPathParent(org.org_path) not in self.org_path_parents and
                org.org_path is not None and
                org.org_path.startswith("/")
                and org.name is not None]

    def update(self, organizations: List[OrganizationReferencesObject] = None):
        if not self.organizations:
            self.organizations = organizations
            self.org_path_parents = [OrgPathParent(org.org_path) for org in self.organizations]

    async def add_organization(self, organization: OrganizationReferencesObject,
                               for_service: ServiceKey = ServiceKey.ORGANIZATIONS):
        if self.organizations is None:
            self.organizations = list()

        if self.org_path_parents is None:
            self.org_path_parents = list()

        if organization.org_path and OrgPathParent(organization.org_path) in self.org_path_parents:
            return None

        stored_organisation = next((o for o in self.organizations if organization.id == o.id), None)

        if stored_organisation:
            stored_organisation.set_count_value(
                for_service=for_service,
                count=stored_organisation.get_count_value(for_service) + organization.get_count_value(for_service)
            )
        else:
            if re.search(r"\d{9}", organization.id):
                if for_service != ServiceKey.ORGANIZATIONS:
                    organization_from_catalog = await get_organization(org_id=organization.id)

                    if organization_from_catalog:
                        organization.update_with_catalog_entry(entry=organization_from_catalog)

                        await self.add_organization(for_service=ServiceKey.ORGANIZATIONS, organization=organization)
                else:
                    if organization.org_path:
                        self.org_path_parents.append(OrgPathParent(organization.org_path))

                    self.organizations.append(organization)

    def get_organization(self, org) -> OrganizationReferencesObject:
        try:
            return self.organizations[self.organizations.index(org)]
        except ValueError:
            return None

    async def add_all(self, organizations: List[OrganizationReferencesObject], for_service: ServiceKey):
        for reference in organizations:
            await self.add_organization(
                organization=reference,
                for_service=for_service
            )

    def clear_content_count(self):
        if self.organizations is None:
            return False
        for org in self.organizations:
            org.clear_count_values()
        return True

    @staticmethod
    def get_instance() -> 'OrganizationStore':
        if OrganizationStore.__instance__:
            return OrganizationStore.__instance__
        else:
            return OrganizationStore()


class OrganizationStoreExistsException(Exception):
    def __init__(self):
        self.message = "organization store is already created"


class OrganizationStoreNotInitiatedException(Exception):
    def __init__(self):
        self.message = "no content in OrganizationStore"

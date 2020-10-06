import asyncio
import re
from typing import List

from src.organization_utils import get_organization
from src.utils import ContentKeys, OrgCatalogKeys, ServiceKey, OrganizationCatalogResult

NATIONAL_REGISTRY_PATTERN = "data.brreg.no/enhetsregisteret"
NATIONAL_REGISTRY_URL = "https://data.brreg.no/enhetsregisteret/api/enheter"
ORGANIZATION_CATALOG_IDENTIFIER_PATTERN = "organization-catalog.[a-z.]*fellesdatakatalog"


class OrganizationReferencesObject:

    def __init__(self,
                 for_service: ServiceKey,
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
        self.id = self.resolve_id()

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
        if type(other) == OrganizationReferencesObject:
            if self.org_uri:
                if self.__eq_on_org_uri(other):
                    return True
                elif self.__eq_on_same_as(other):
                    return True
                elif self.org_path and other.org_path:
                    return self.org_path == other.org_path
                elif self.name and other.name:
                    return self.name.upper() == other.name.upper()
            elif self.same_as and other.same_as and self.__eq_on_same_as(other):
                return True
            elif self.org_path and other.org_path:
                return self.org_path == other.org_path
            elif self.name and other.name:
                return self.name.upper() == other.name.upper()
        elif type(other) == str:
            if not self.org_path:
                return False
            else:
                return self.org_path == other
        else:
            return False

    def __eq_on_org_uri(self, other: 'OrganizationReferencesObject'):
        if not other.org_uri:
            return False
        return OrganizationReferencesObject.__eq_on_national_registry(
            self.org_uri,
            other.org_uri)

    def __eq_on_same_as(self, other: 'OrganizationReferencesObject'):
        if not self.same_as:
            return False
        if not other.same_as:
            return False
        else:
            matches = [org for org in self.same_as if org in other.same_as]
            return len(matches) > 0

    @staticmethod
    def __eq_on_http(uri_1: str, uri_2: str) -> bool:
        if NATIONAL_REGISTRY_PATTERN in uri_1 and NATIONAL_REGISTRY_PATTERN in uri_2:
            return OrganizationReferencesObject.__eq_on_national_registry(uri_1, uri_2)
        suffix_1 = uri_1.split("//")[1]
        suffix_2 = uri_2.split("//")[1]
        return suffix_1 == suffix_2

    @staticmethod
    def __eq_on_national_registry(uri_1: str, uri_2: str) -> bool:
        suffix_1 = uri_1.split("/")
        suffix_2 = uri_2.split("/")
        return suffix_1[- 1] == suffix_2[- 1]

    @staticmethod
    def from_organization_catalog_single_response(organization: dict):
        return OrganizationReferencesObject(
            for_service=ServiceKey.ORGANIZATIONS,
            org_uri=organization[OrgCatalogKeys.URI],
            org_path=organization[OrgCatalogKeys.ORG_PATH],
            name=organization[OrgCatalogKeys.NAME]
        )

    @staticmethod
    def from_organization_catalog_list_response(organizations: List[dict]):
        return [OrganizationReferencesObject.from_organization_catalog_single_response(org) for org in organizations]

    @staticmethod
    def from_sparql_query_result(for_service: ServiceKey, organization: dict) -> 'OrganizationReferencesObject':
        keys = organization.keys()
        try:
            name = organization.get(ContentKeys.ORG_NAME).get(ContentKeys.VALUE)
        except AttributeError:
            name = None
        count = organization.get(ContentKeys.COUNT).get(ContentKeys.VALUE)
        reference_object = OrganizationReferencesObject(for_service=for_service, name=name, count=int(count))
        if ContentKeys.PUBLISHER in keys:
            publisher_uri = organization.get(ContentKeys.PUBLISHER).get(ContentKeys.VALUE)
            national_registry_uri = OrganizationReferencesObject.resolve_national_registry_uri(publisher_uri)
            if national_registry_uri:
                reference_object.org_uri = national_registry_uri
            else:
                reference_object.same_as.append(publisher_uri)
        if ContentKeys.SAME_AS in keys:
            same_as_uri = organization.get(ContentKeys.SAME_AS).get(ContentKeys.VALUE)
            national_registry_uri = OrganizationReferencesObject.resolve_national_registry_uri(same_as_uri)
            if national_registry_uri:
                reference_object.org_uri = national_registry_uri
            else:
                reference_object.same_as.append(reference_object)
        return reference_object

    @staticmethod
    def from_sparql_bindings(for_service: ServiceKey, sparql_bindings: List[dict]):
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
    def from_es_response_list(es_response: List[dict], for_service) -> List['OrganizationReferencesObject']:
        return [OrganizationReferencesObject.from_es_bucket(for_service=for_service,
                                                            es_bucket=bucket)
                for bucket in es_response[ContentKeys.AGGREGATIONS][ContentKeys.ORG_PATH][ContentKeys.BUCKETS]
                ]

    @staticmethod
    def resolve_national_registry_uri(uri):
        if uri is None:
            return False
        prefix = uri.split(":")[1]
        if NATIONAL_REGISTRY_PATTERN in prefix:
            return uri
        else:
            return OrganizationReferencesObject.resolve_organization_catalog_uri(uri)

    @staticmethod
    def resolve_organization_catalog_uri(uri):
        if re.search(ORGANIZATION_CATALOG_IDENTIFIER_PATTERN, uri):
            org_id = uri.split("/")[-1]
            return f"{NATIONAL_REGISTRY_URL}/{org_id}".strip()
        else:
            return False

    def resolve_id(self):
        if self.org_uri and OrganizationReferencesObject.is_national_registry_uri(self.org_uri):
            return self.org_uri.split("/")[-1]
        elif self.org_path:
            return self.org_path.split("/")[-1]
        else:
            return None

    def resolve_display_id(self):
        return self.id or self.name

    @staticmethod
    def is_national_registry_uri(uri):
        if uri is None:
            return False
        try:
            prefix = uri.split(":")[1]
            if NATIONAL_REGISTRY_PATTERN in prefix:
                return True
            elif OrganizationReferencesObject.resolve_organization_catalog_uri(uri):
                return True
            else:
                return False
        except IndexError:
            return False

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
        if organization.org_path:
            if OrgPathParent(organization.org_path) in self.org_path_parents:
                return None
        try:
            org_idx = self.organizations.index(organization)
            stored_org: OrganizationReferencesObject = self.organizations[org_idx]
            new_content_count = stored_org.get_count_value(for_service) + organization.get_count_value(for_service)
            stored_org.set_count_value(for_service=for_service,
                                       count=new_content_count)
            if len(organization.same_as) > 0:
                stored_org.same_as.extend(organization.same_as)
        except ValueError:
            if for_service != ServiceKey.ORGANIZATIONS:
                from_catalog = await get_organization(org_id=organization.id, name=organization.name)
                if from_catalog and OrgPathParent(from_catalog.org_path) not in self.org_path_parents:
                    organization.update_with_catalog_entry(entry=from_catalog)
                    await self.add_organization(for_service=ServiceKey.ORGANIZATIONS, organization=organization)
            else:
                self.__append_new_organization(organization)

    def __append_new_organization(self, organization: OrganizationReferencesObject):
        self.organizations.append(organization)
        if organization.org_path:
            self.org_path_parents.append(OrgPathParent(organization.org_path))
        org_idx = self.organizations.index(organization)
        if len(organization.same_as) > 0:
            self.organizations[org_idx].same_as.extend(organization.same_as)

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

import re
from typing import List
from src.utils import ContentKeys, OrgCatalogKeys, ServiceKey

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
        self.dataset_count = count if for_service == ServiceKey.DATA_SETS else 0
        self.dataservice_count = count if for_service == ServiceKey.DATA_SERVICES else 0
        self.concept_count = count if for_service == ServiceKey.CONCEPTS else 0
        self.informationmodel_count = count if for_service == ServiceKey.INFO_MODELS else 0
        self.id = OrganizationReferencesObject.resolve_id(org_uri)

    def set_count_value(self, for_service: ServiceKey, count):
        if for_service == ServiceKey.DATA_SETS:
            self.dataset_count = int(count)
        elif for_service == ServiceKey.DATA_SERVICES:
            self.dataservice_count = int(count)
        elif for_service == ServiceKey.INFO_MODELS:
            self.informationmodel_count = count
        elif for_service == ServiceKey.CONCEPTS:
            self.concept_count = count

    def get_count_value(self, for_service: ServiceKey) -> int:
        if for_service == ServiceKey.DATA_SETS:
            return self.dataset_count
        elif for_service == ServiceKey.DATA_SERVICES:
            return self.dataservice_count
        elif for_service == ServiceKey.INFO_MODELS:
            return self.informationmodel_count
        elif for_service == ServiceKey.CONCEPTS:
            return self.concept_count

    def __eq__(self, other):
        if type(other) == OrganizationReferencesObject:
            if self.org_uri:
                if self.__eq_on_org_uri(other):
                    return True
                elif self.__eq_on_same_as(other):
                    return True
                elif self.org_path and other.org_path:
                    return self.org_path == other.org_path

            elif self.same_as and other.same_as:
                return self.__eq_on_same_as(other)
            elif self.org_path and other.org_path:
                return self.org_path == other.org_path
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
    def from_es_response(for_service: ServiceKey, es_response: dict):
        return OrganizationReferencesObject(
            for_service=for_service,
            org_path=es_response[ContentKeys.KEY],
            count=es_response[ContentKeys.COUNT]
        )

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
            return f"{NATIONAL_REGISTRY_URL}/{org_id}"
        else:
            return False

    @staticmethod
    def resolve_id(uri: str):
        if uri:
            uri_parts = uri.split("/")
            return uri_parts[-1]
        else:
            return None


class OrgPathParent:
    def __init__(self, org_path: str):
        self.org_path_joints = org_path.split("/")

    def __eq__(self, other: 'OrgPathParent'):
        if len(other.org_path_joints) > len(self.org_path_joints):
            for idx, joint in enumerate(self.org_path_joints):
                if other.org_path_joints[idx] != joint:
                    return False
            return True
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
        return [org for org in self.organizations if OrgPathParent(org.org_path) not in self.org_path_parents]

    def update(self, organizations: List[OrganizationReferencesObject] = None):
        if not self.organizations:
            self.organizations = organizations
            self.org_path_parents = [OrgPathParent(org.org_path) for org in self.organizations]

    def add_organization(self, organization: OrganizationReferencesObject,
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
            stored_org.set_count_value(for_service=for_service,
                                       count=organization.get_count_value(for_service=for_service))
        except ValueError:
            self.organizations.append(organization)
            if organization.org_path:
                self.org_path_parents.append(OrgPathParent(organization.org_path))
            org_idx = self.organizations.index(organization)
        if len(organization.same_as) > 0:
            self.organizations[org_idx].same_as.extend(organization.same_as)

    def get_orgpath(self, uri: str) -> str:
        try:
            org_idx = self.organizations.index(uri)
            return self.organizations[org_idx].org_path
        except ValueError:
            return None
        except AttributeError:
            raise OrganizationStoreNotInitiatedException()

    def get_organization(self, org) -> OrganizationReferencesObject:
        try:
            return self.organizations[self.organizations.index(org)]
        except ValueError:
            return None

    def add_all_publishers(self, publishers: List[dict]):
        for reference in publishers["results"]["bindings"]:
            self.add_organization(
                OrganizationReferencesObject.from_sparql_query_result(reference))

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

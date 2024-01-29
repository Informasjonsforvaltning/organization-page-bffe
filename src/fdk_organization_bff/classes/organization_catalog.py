"""Organization catalog data class."""

from dataclasses import dataclass
from typing import Optional

from fdk_organization_bff.classes.organization_concepts import OrganizationConcepts
from fdk_organization_bff.classes.organization_dataservices import (
    OrganizationDataservices,
)
from fdk_organization_bff.classes.organization_datasets import OrganizationDatasets
from fdk_organization_bff.classes.organization_details import OrganizationDetails
from fdk_organization_bff.classes.organization_informationmodels import (
    OrganizationInformationmodels,
)


@dataclass
class OrganizationCatalog:
    """Data class wrapping an organization and its catalogs."""

    organization: Optional[OrganizationDetails]
    datasets: OrganizationDatasets
    dataservices: OrganizationDataservices
    concepts: OrganizationConcepts
    informationmodels: OrganizationInformationmodels

"""Organization catalog summary data class."""
from dataclasses import dataclass
from typing import Dict


@dataclass
class OrganizationCatalogSummary:
    """Data class with summary of an organization and its published catalogs."""

    id: str
    name: str
    prefLabel: Dict
    orgPath: str
    datasetCount: int
    conceptCount: int
    dataserviceCount: int
    informationmodelCount: int

    def sort_compare(self: "OrganizationCatalogSummary") -> str:
        """Get value for sorting."""
        nb = self.prefLabel.get("nb")
        return nb if nb else self.name

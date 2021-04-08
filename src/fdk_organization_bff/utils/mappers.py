"""Mapper module."""
import logging
from typing import Dict, List, Optional

from fdk_organization_bff.classes import (
    CatalogQualityRating,
    OrganizationDatasets,
    OrganizationDetails,
)
from fdk_organization_bff.utils.utils import (
    dataset_has_national_provenance,
    dataset_is_new,
    dataset_is_open,
)


def map_catalog_quality_rating(
    assessment_data: Dict,
) -> Optional[CatalogQualityRating]:
    """Map data from fdk-metadata-quality-service to CatalogQualityRating."""
    score = assessment_data.get("score")
    max_score = assessment_data.get("maxScore")
    category = assessment_data.get("category")
    if score and max_score and category:
        try:
            return CatalogQualityRating(
                category=category,
                percentage=int(round(100 * (int(score) / int(max_score))))
                if score and max_score
                else None,
            )
        except BaseException:
            logging.error("bad data from fdk-metadata-quality-service", assessment_data)
    return None


def map_org_datasets(
    org_datasets: List,
    assessment_data: Dict,
    open_licenses: List,
) -> OrganizationDatasets:
    """Map data from fdk-sparql-service and fdk-metadata-quality-service to OrganizationDatasets."""
    authoritative_datasets = 0
    new_datasets = 0
    open_datasets = 0

    for dataset in org_datasets:
        if dataset_has_national_provenance(dataset):
            authoritative_datasets += 1
        if dataset_is_new(dataset):
            new_datasets += 1
        if dataset_is_open(dataset, open_licenses):
            open_datasets += 1

    return OrganizationDatasets(
        total=len(org_datasets),
        new=new_datasets,
        authoritative=authoritative_datasets,
        open=open_datasets,
        quality=map_catalog_quality_rating(assessment_data),
    )


def map_org_details(
    org_cat_data: Dict, brreg_data: Dict
) -> Optional[OrganizationDetails]:
    """Map data from Enhetsregisteret and organization-catalogue to OrganizationDetails."""
    organization_id = org_cat_data.get("organizationId")
    if organization_id:
        org_id = str(organization_id)
        pref_label = org_cat_data.get("prefLabel")
        org_type = None
        sector_code = None
        industry_code = None
        homepage = None
        see_also = None

        if brreg_data:
            orgform = brreg_data.get("organisasjonsform")
            org_type = orgform.get("beskrivelse") if orgform else None

            naeringskode = brreg_data.get("naeringskode1")
            industry_code = (
                f"""{naeringskode.get("kode")} {naeringskode.get("beskrivelse")}"""
                if naeringskode
                else None
            )

            sektorkode = brreg_data.get("institusjonellSektorkode")
            sector_code = (
                f"""{sektorkode.get("kode")} {sektorkode.get("beskrivelse")}"""
                if sektorkode
                else None
            )

            homepage = brreg_data.get("hjemmeside")

            see_also = (
                f"https://data.brreg.no/enhetsregisteret/oppslag/enheter/{org_id}"
            )

        name = org_cat_data.get("name")
        org_path = org_cat_data.get("orgPath")

        return OrganizationDetails(
            name=str(name) if name else None,
            organizationId=org_id,
            prefLabel=dict(pref_label) if pref_label else dict(),
            orgPath=str(org_path) if org_path else None,
            orgType=str(org_type) if org_type else None,
            sectorCode=sector_code,
            industryCode=industry_code,
            homepage=str(homepage) if homepage else None,
            seeAlso=see_also,
            icon=f"https://orglogo.difi.no/api/logo/org/{org_id}",
        )
    else:
        return None

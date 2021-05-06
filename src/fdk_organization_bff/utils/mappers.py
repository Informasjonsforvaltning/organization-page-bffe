"""Mapper module."""
import logging
from typing import Dict, List, Optional

from fdk_organization_bff.classes import (
    CatalogQualityRating,
    OrganizationCatalogSummary,
    OrganizationDatasets,
    OrganizationDetails,
)
from fdk_organization_bff.utils.utils import (
    dataset_is_authoritative,
    dataset_is_new,
    dataset_is_open_data,
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
) -> OrganizationDatasets:
    """Map data from fdk-sparql-service and fdk-metadata-quality-service to OrganizationDatasets."""
    datasets = set()
    authoritative_datasets = set()
    new_datasets = set()
    open_datasets = set()

    for dataset in org_datasets:
        dataset_uri = dataset["dataset"]["value"]
        datasets.add(dataset_uri)
        if dataset_is_authoritative(dataset):
            authoritative_datasets.add(dataset_uri)
        if dataset_is_new(dataset):
            new_datasets.add(dataset_uri)
        if dataset_is_open_data(dataset):
            open_datasets.add(dataset_uri)

    return OrganizationDatasets(
        totalCount=len(datasets),
        newCount=len(new_datasets),
        authoritativeCount=len(authoritative_datasets),
        openCount=len(open_datasets),
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


def count_list_from_sparql_response(sparql_response: Dict) -> List:
    """Map sparql-response to list of orgId and count value."""
    results = sparql_response.get("results")
    bindings = results.get("bindings") if results else []
    result_list = bindings if bindings else []
    mapped_list = [
        org_and_count_value_from_sparql_response(item) for item in result_list
    ]
    return list(filter(None, mapped_list))


def org_and_count_value_from_sparql_response(sparql_response: Dict) -> Optional[Dict]:
    """Map sparql-response to dict with orgId and count value."""
    org = sparql_response.get("organizationNumber")
    org_value = org.get("value") if org else None
    count = sparql_response.get("count")
    count_value = count.get("value") if count else None

    return (
        {"org": org_value.strip().replace(" ", ""), "count": count_value}
        if org_value and count_value
        else None
    )


def map_org_summary(
    org_id: str, org_counts: Dict, org_data: Optional[Dict]
) -> OrganizationCatalogSummary:
    """Map data from organization-catalogue and counts from sparql-queries to OrganizationCatalogSummary."""
    dataset_count = int(org_counts["datasets"]) if org_counts.get("datasets") else 0
    dataservice_count = (
        int(org_counts["dataservices"]) if org_counts.get("dataservices") else 0
    )

    return OrganizationCatalogSummary(
        id=org_id,
        name=org_data["name"] if org_data else org_id,
        prefLabel=org_data["prefLabel"] if org_data else dict(),
        datasetCount=dataset_count,
        conceptCount=0,
        dataserviceCount=dataservice_count,
        informationmodelCount=0,
    )


def map_org_summaries(
    organizations: Dict,
    datasets: List,
    dataservices: List,
) -> List[OrganizationCatalogSummary]:
    """Map data from fdk-sparql-service and organization-ctalogue to a list of OrganizationCatalogSummary."""
    org_counts = {count["org"]: {"datasets": count["count"]} for count in datasets}

    for count in dataservices:
        if org_counts.get(count["org"]):
            org_counts[count["org"]]["dataservices"] = count["count"]
        else:
            org_counts[count["org"]] = {"dataservices": count["count"]}

    return [
        map_org_summary(org_id, org_counts[org_id], organizations.get(org_id))
        for org_id in org_counts
    ]

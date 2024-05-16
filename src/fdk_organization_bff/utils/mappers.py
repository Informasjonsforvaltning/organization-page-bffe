"""Mapper module."""

import logging
import traceback
from typing import Dict, List, Optional

from fdk_organization_bff.classes import (
    CatalogQualityScore,
    OrganizationCatalogSummary,
    OrganizationCategory,
    OrganizationConcepts,
    OrganizationDataservices,
    OrganizationDatasets,
    OrganizationDetails,
    OrganizationInformationmodels,
)
from fdk_organization_bff.utils.utils import (
    dataset_is_authoritative,
    dataset_is_open_data,
    resource_is_new,
    to_int,
)


def map_catalog_quality_score(
    score_data: Dict,
) -> Optional[CatalogQualityScore]:
    """Map data from fdk-mqa-score-api to CatalogQualityScore."""
    score = 0
    max_score = 0

    try:
        if "aggregations" in score_data:
            for agg in score_data["aggregations"]:
                if "score" in agg:
                    score = score + int(agg["score"])
                if "max_score" in agg:
                    max_score = max_score + int(agg["max_score"])
    except ValueError:
        logging.error(
            f"{traceback.format_exc()}: bad data from fdk-mqa-score-api {score_data}"
        )

    if score and max_score:
        return CatalogQualityScore(
            score=score,
            percentage=(
                int(round(100 * (int(score) / int(max_score))))
                if score and max_score
                else None
            ),
        )

    return None


def map_org_datasets(
    org_datasets: List,
    score_data: Dict,
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
        if resource_is_new(dataset):
            new_datasets.add(dataset_uri)
        if dataset_is_open_data(dataset):
            open_datasets.add(dataset_uri)

    return OrganizationDatasets(
        totalCount=len(datasets),
        newCount=len(new_datasets),
        authoritativeCount=len(authoritative_datasets),
        openCount=len(open_datasets),
        quality=map_catalog_quality_score(score_data),
    )


def empty_datasets() -> OrganizationDatasets:
    """Empty response for OrganizationDatasets."""
    return OrganizationDatasets(
        totalCount=0,
        newCount=0,
        authoritativeCount=0,
        openCount=0,
        quality=None,
    )


def map_org_details(
    org_cat_data: Dict, brreg_data: Dict
) -> Optional[OrganizationDetails]:
    """Map data from Enhetsregisteret and organization-catalog to OrganizationDetails."""
    organization_id = org_cat_data.get("organizationId")
    if organization_id:
        org_id = str(organization_id)
        pref_label = org_cat_data.get("prefLabel")
        org_type = None
        sector_code = None
        industry_code = None
        homepage = None
        see_also = None
        number_of_employees = None

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

            number_of_employees = to_int(brreg_data.get("antallAnsatte"))

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
            numberOfEmployees=number_of_employees if number_of_employees else None,
            icon=f"https://orglogo.digdir.no/api/logo/org/{org_id}",
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
    org_id: str, org_counts: Optional[Dict], org_data: Optional[Dict]
) -> OrganizationCatalogSummary:
    """Map data from organization-catalog and counts from sparql-queries to OrganizationCatalogSummary."""
    org_counts = dict() if org_counts is None else org_counts
    dataset_count = int(org_counts["datasets"]) if org_counts.get("datasets") else 0
    dataservice_count = (
        int(org_counts["dataservices"]) if org_counts.get("dataservices") else 0
    )
    concept_count = int(org_counts["concepts"]) if org_counts.get("concepts") else 0
    informationmodel_count = (
        int(org_counts["informationmodels"])
        if org_counts.get("informationmodels")
        else 0
    )

    return OrganizationCatalogSummary(
        id=org_id,
        name=org_data["name"] if org_data else org_id,
        prefLabel=org_data["prefLabel"] if org_data else dict(),
        orgPath=org_data["orgPath"] if org_data else "",
        datasetCount=dataset_count,
        conceptCount=concept_count,
        dataserviceCount=dataservice_count,
        informationmodelCount=informationmodel_count,
    )


def add_org_counts(label: str, sparql_results: List, org_counts: Dict) -> Dict:
    """Add counts for organization by entity type."""
    for count in sparql_results:
        if org_counts.get(count["org"]):
            org_counts[count["org"]][label] = count["count"]
        else:
            org_counts[count["org"]] = {label: count["count"]}
    return org_counts


def map_org_summaries(
    organizations: Dict,
    datasets: List,
    dataservices: List,
    concepts: List,
    informationmodels: List,
    include_empty: bool,
) -> List[OrganizationCatalogSummary]:
    """Map data from fdk-sparql-service and organization-ctalogue to a list of OrganizationCatalogSummary."""
    org_counts = add_org_counts("datasets", datasets, {})
    org_counts = add_org_counts("dataservices", dataservices, org_counts)
    org_counts = add_org_counts("concepts", concepts, org_counts)
    org_counts = add_org_counts("informationmodels", informationmodels, org_counts)

    if include_empty:
        summaries: List[OrganizationCatalogSummary] = list()
        for org_id in organizations:
            if org_counts.get(org_id) is not None or org_is_stat_fylk_or_komm(
                organizations[org_id]
            ):
                summaries.append(
                    map_org_summary(
                        org_id, org_counts.get(org_id), organizations[org_id]
                    )
                )
        return summaries
    else:
        return [
            map_org_summary(org_id, org_counts[org_id], organizations.get(org_id))
            for org_id in org_counts
        ]


def categorise_summaries_by_parent_org(
    summaries: List[OrganizationCatalogSummary], include_empty: bool
) -> List[OrganizationCategory]:
    """Categorise summaries by parent organization."""
    categorised_summaries: Dict[str, List[OrganizationCatalogSummary]] = dict()
    for summary in summaries:
        org_path_split = summary.orgPath.split("/")
        if len(org_path_split) > 2:
            main_org = summary.orgPath.split("/")[2]
            list_by_main_org = categorised_summaries.get(main_org, [])
            list_by_main_org.append(summary)
            categorised_summaries[main_org] = list_by_main_org
        else:
            logging.warning(f"invalid orgPath for {summary.id}")

    categories: List[OrganizationCategory] = list()
    for main_org in categorised_summaries:
        category = OrganizationCatalogSummary(
            id=main_org,
            name="",
            prefLabel={},
            orgPath="",
            datasetCount=0,
            conceptCount=0,
            dataserviceCount=0,
            informationmodelCount=0,
        )

        for summary in categorised_summaries[main_org]:
            category.datasetCount += summary.datasetCount
            category.conceptCount += summary.conceptCount
            category.dataserviceCount += summary.dataserviceCount
            category.informationmodelCount += summary.informationmodelCount
            if summary.id == main_org:
                category.name = summary.name
                category.prefLabel = summary.prefLabel
                category.orgPath = summary.orgPath

        category_summaries = (
            categorised_summaries[main_org]
            if include_empty
            else remove_empty_summaries(categorised_summaries[main_org])
        )

        categories.append(
            OrganizationCategory(
                category=category,
                organizations=sorted(
                    category_summaries, key=lambda org: org.sort_compare()
                ),
            )
        )

    return sorted(categories, key=lambda org: org.sort_compare())


def categorise_summaries_by_municipality(
    summaries: List[OrganizationCatalogSummary],
    municipalities: Dict,
    include_empty: bool,
) -> List[OrganizationCategory]:
    """Categorise summaries by municipalities."""
    categories_dict: Dict[str, OrganizationCategory] = dict()
    categorized_organization_numbers = dict()
    filtered_summaries = (
        summaries if include_empty else remove_empty_summaries(summaries)
    )
    for fylke in municipalities["fylke"]:
        categories_dict[fylke["fylkesnummer"]] = OrganizationCategory(
            category=OrganizationCatalogSummary(
                id=fylke["organisasjonsnummer"],
                name=fylke["fylkesnavn"],
                prefLabel={"nb": fylke["fylkesnavn"]},
                orgPath="/FYLKE/" + fylke["organisasjonsnummer"],
                datasetCount=0,
                conceptCount=0,
                dataserviceCount=0,
                informationmodelCount=0,
            ),
            organizations=list(),
        )
        categorized_organization_numbers[fylke["organisasjonsnummer"]] = fylke[
            "fylkesnummer"
        ]

    for kommune in municipalities["kommune"]:
        categorized_organization_numbers[kommune["organisasjonsnummer"]] = kommune[
            "kommunenummer"
        ][:2]

    for org_summary in filtered_summaries:
        org_path_split = org_summary.orgPath.split("/")
        category_number = (
            categorized_organization_numbers.get(org_path_split[2], "")
            if len(org_path_split) > 2
            else ""
        )
        municipality_category = categories_dict.get(category_number)
        if municipality_category:
            municipality_category.category.datasetCount += org_summary.datasetCount
            municipality_category.category.conceptCount += org_summary.conceptCount
            municipality_category.category.dataserviceCount += (
                org_summary.dataserviceCount
            )
            municipality_category.category.informationmodelCount += (
                org_summary.informationmodelCount
            )
            municipality_category.organizations.append(org_summary)
            categories_dict[category_number] = municipality_category

    categories: List[OrganizationCategory] = list()
    for key in categories_dict:
        categories_dict[key].organizations = sorted(
            categories_dict[key].organizations, key=lambda org: org.sort_compare()
        )
        categories.append(categories_dict[key])

    return sorted(categories, key=lambda org: org.sort_compare())


def remove_empty_summaries(
    summaries: List[OrganizationCatalogSummary],
) -> List[OrganizationCatalogSummary]:
    """Remove all empty summaries from list."""
    filtered: List[OrganizationCatalogSummary] = list()
    for summary in summaries:
        if (
            summary.datasetCount > 0
            or summary.conceptCount > 0
            or summary.dataserviceCount > 0
            or summary.informationmodelCount > 0
        ):
            filtered.append(summary)
    return filtered


def org_is_stat_fylk_or_komm(org: Dict) -> bool:
    """Check if an organization has orgPath with type STAT, KOMMUNE or FYLKE."""
    org_path = org.get("orgPath")
    if org_path is None:
        return False
    elif "/STAT/" in org_path:
        return True
    elif "/FYLKE/" in org_path:
        return True
    elif "/KOMMUNE/" in org_path:
        return True
    else:
        return False


def map_org_dataservices(
    org_dataservices: List,
) -> OrganizationDataservices:
    """Map data from fdk-sparql-service to OrganizationDataservices."""
    services = set()
    new_services = set()

    for service in org_dataservices:
        service_uri = service["service"]["value"]
        services.add(service_uri)
        if resource_is_new(service):
            new_services.add(service_uri)

    return OrganizationDataservices(
        totalCount=len(services),
        newCount=len(new_services),
    )


def empty_dataservices() -> OrganizationDataservices:
    """Empty response for OrganizationDataservices."""
    return OrganizationDataservices(
        totalCount=0,
        newCount=0,
    )


def map_org_concepts(
    org_concepts: List,
) -> OrganizationConcepts:
    """Map data from fdk-sparql-concept to OrganizationConcepts."""
    concepts = set()
    new_concepts = set()

    for concept in org_concepts:
        concept_uri = concept["concept"]["value"]
        concepts.add(concept_uri)
        if resource_is_new(concept):
            new_concepts.add(concept_uri)

    return OrganizationConcepts(
        totalCount=len(concepts),
        newCount=len(new_concepts),
    )


def empty_concepts() -> OrganizationConcepts:
    """Empty response for OrganizationConcepts."""
    return OrganizationConcepts(
        totalCount=0,
        newCount=0,
    )


def map_org_informationmodels(
    org_informationmodels: List,
) -> OrganizationInformationmodels:
    """Map data from fdk-sparql-informationmodel to OrganizationInformationmodel."""
    informationmodels = set()
    new_informationmodels = set()

    for informationmodel in org_informationmodels:
        informationmodel_uri = informationmodel["informationmodel"]["value"]
        informationmodels.add(informationmodel_uri)
        if resource_is_new(informationmodel):
            new_informationmodels.add(informationmodel_uri)

    return OrganizationInformationmodels(
        totalCount=len(informationmodels),
        newCount=len(new_informationmodels),
    )


def empty_informationmodels() -> OrganizationInformationmodels:
    """Empty response for OrganizationInformationmodel."""
    return OrganizationInformationmodels(
        totalCount=0,
        newCount=0,
    )

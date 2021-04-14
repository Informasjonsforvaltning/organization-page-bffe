"""Util module."""
import datetime
import logging
from typing import Dict, List, Optional
from urllib.parse import quote_plus

from fdk_organization_bff.classes import FilterEnum


def url_with_params(url: str, params: Optional[Dict[str, str]]) -> str:
    """Add parameters to a URL."""
    if params and len(params) > 0:
        params_list = []
        for key in params:
            params_list.append(f"{key}={quote_plus(params[key])}")

        seperator = "&"
        return f"{url}?{seperator.join(params_list)}"
    else:
        return url


def filter_param_to_enum(param: Optional[str]) -> FilterEnum:
    """Map filter param value to corresponding enum."""
    if param is None:
        return FilterEnum.NONE
    elif param == FilterEnum.NAP.value:
        return FilterEnum.NAP
    else:
        return FilterEnum.INVALID


def dataset_has_national_provenance(dataset: Dict) -> bool:
    """Check if dataset has national provenance."""
    dataset_provenance = dataset.get("provenance")
    if dataset_provenance:
        national_provenance = "http://data.brreg.no/datakatalog/provinens/nasjonal"
        return dataset_provenance["value"] == national_provenance
    return False


def dataset_is_new(dataset: Dict) -> bool:
    """Check if dataset was first published within the last 7 days."""
    issued = dataset.get("issued")
    if issued:
        date_format = "%Y-%m-%d"
        try:
            issued_date = datetime.datetime.strptime(
                issued["value"][0:10], date_format
            ).date()
            seven_days_ago = datetime.date.today() - datetime.timedelta(days=7)
            return issued_date >= seven_days_ago
        except BaseException:
            logging.error("failed to parse dataset issued date")
    return False


def dataset_is_open(dataset: Dict, open_licenses: List) -> bool:
    """Check if dataset has public access rights and a distribution with an open license."""
    dataset_rights = dataset.get("rights")
    distribution_license = dataset.get("licenseSource")
    if dataset_rights and distribution_license:
        public = "http://publications.europa.eu/resource/authority/access-right/PUBLIC"
        if dataset_rights["value"] != public:
            return False
        else:
            return distribution_license["value"] in open_licenses

    return False

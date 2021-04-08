"""Util module."""
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional


def url_with_params(url: str, params: Optional[Dict[str, str]]) -> str:
    """Add parameters to a URL."""
    if params and len(params) > 0:
        params_list = []
        for key in params:
            params_list.append(f"{key}={params[key]}")

        seperator = "&"
        return f"{url}?{seperator.join(params_list)}"
    else:
        return url


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
        date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        try:
            issued_date = datetime.strptime(issued["value"], date_format).date()
            seven_days_ago = (datetime.now() - timedelta(days=7)).date()
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

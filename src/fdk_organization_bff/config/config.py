"""Configure fdk-organization-bff."""
import os
from typing import Dict, List, Type, TypeVar


T = TypeVar("T", bound="Config")


class Config:
    """Configuration class."""

    _ORG_CATALOG_PATH = "/organizationcatalogs"

    _ROUTES = {
        "PING": "/ping",
        "READY": "/ready",
        "ORG_CATALOG": _ORG_CATALOG_PATH + "/{id}",
        "ORG_CATALOGS": _ORG_CATALOG_PATH,
    }
    _ORGANIZATION_CATALOGUE_URI = os.getenv(
        "ORGANIZATION_CATALOGUE_URI",
        "https://organization-catalogue.staging.fellesdatakatalog.digdir.no",
    )
    _DATA_BRREG_URI = os.getenv(
        "DATA_BRREG_URI",
        "https://data.brreg.no",
    )
    _FDK_PORTAL_URI = os.getenv(
        "FDK_PORTAL_URI",
        "https://staging.fellesdatakatalog.digdir.no",
    )
    _FDK_SPARQL_URI = os.getenv(
        "FDK_SPARQL_URI",
        "https://sparql.staging.fellesdatakatalog.digdir.no",
    )
    _FDK_METADATA_QUALITY_URI = os.getenv(
        "FDK_METADATA_QUALITY_URI",
        "https://metadata-quality.staging.fellesdatakatalog.digdir.no",
    )
    _NAP_THEMES = [
        '"https://psi.norge.no/los/tema/mobilitetstilbud"',
        '"https://psi.norge.no/los/tema/trafikkinformasjon"',
        '"https://psi.norge.no/los/tema/veg-og-vegregulering"',
        '"https://psi.norge.no/los/tema/yrkestransport"',
        '"https://psi.norge.no/los/ord/ruteinformasjon"',
        '"https://psi.norge.no/los/ord/lokasjonstjenester"',
        '"https://psi.norge.no/los/ord/tilrettelagt-transport"',
        '"https://psi.norge.no/los/ord/miljovennlig-transport"',
        '"https://psi.norge.no/los/ord/takster-og-kjopsinformasjon"',
        '"https://psi.norge.no/los/ord/reisegaranti"',
        '"https://psi.norge.no/los/ord/reisebillett"',
        '"https://psi.norge.no/los/ord/parkering-og-hvileplasser"',
        '"https://psi.norge.no/los/ord/drivstoff-og-ladestasjoner"',
        '"https://psi.norge.no/los/ord/skoleskyss"',
        '"https://psi.norge.no/los/ord/ruteplanlegger"',
        '"https://psi.norge.no/los/ord/veg--og-foreforhold"',
        '"https://psi.norge.no/los/ord/sanntids-trafikkinformasjon"',
        '"https://psi.norge.no/los/ord/bominformasjon"',
        '"https://psi.norge.no/los/ord/trafikksignaler-og-reguleringer"',
        '"https://psi.norge.no/los/ord/vegarbeid"',
        '"https://psi.norge.no/los/ord/trafikksikkerhet"',
        '"https://psi.norge.no/los/ord/persontransport"',
        '"https://psi.norge.no/los/ord/godstransport"',
        '"https://psi.norge.no/los/ord/feiing-og-stroing"',
        '"https://psi.norge.no/los/ord/aksellastrestriksjoner"',
        '"https://psi.norge.no/los/ord/broyting"',
        '"https://psi.norge.no/los/ord/gangveg"',
        '"https://psi.norge.no/los/ord/vegnett"',
        '"https://psi.norge.no/los/ord/gatelys"',
        '"https://psi.norge.no/los/ord/vegbygging"',
        '"https://psi.norge.no/los/ord/privat-vei"',
        '"https://psi.norge.no/los/ord/vegvedlikehold"',
        '"https://psi.norge.no/los/ord/gravemelding"',
        '"https://psi.norge.no/los/ord/sykkel"',
    ]

    @classmethod
    def routes(cls: Type[T]) -> Dict[str, str]:
        """Return a dict with route-value for available views."""
        return cls._ROUTES

    @classmethod
    def org_cat_uri(cls: Type[T]) -> str:
        """Organization Catalogue URI."""
        return cls._ORGANIZATION_CATALOGUE_URI

    @classmethod
    def data_brreg_uri(cls: Type[T]) -> str:
        """BRREG URI."""
        return cls._DATA_BRREG_URI

    @classmethod
    def portal_uri(cls: Type[T]) -> str:
        """FDK Portal URI."""
        return cls._FDK_PORTAL_URI

    @classmethod
    def sparql_uri(cls: Type[T]) -> str:
        """FDK SPARQL URI."""
        return cls._FDK_SPARQL_URI

    @classmethod
    def metadata_uri(cls: Type[T]) -> str:
        """FDK Metadata Quality Service URI."""
        return cls._FDK_METADATA_QUALITY_URI

    @classmethod
    def nap_themes(cls: Type[T]) -> List[str]:
        """List of NAP-themes."""
        return cls._NAP_THEMES

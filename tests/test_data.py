from src.result_readers import ParsedContent

org_1: dict = {
    "organizationId": "974760673",
    "norwegianRegistry": "https://data.brreg.no/enhetsregisteret/api/enheter/974760673",
    "internationalRegistry": None,
    "name": "REGISTERENHETEN I BRØNNØYSUND",
    "orgType": "ORGL",
    "orgPath": "/STAT/912660680/974760673",
    "subOrganizationOf": "912660680",
    "issued": "1995-08-09",
    "municipalityNumber": "1813",
    "industryCode": "84.110",
    "sectorCode": "6100",
    "prefLabel": None,
    "allowDelegatedRegistration": None
}
org_2: dict = {
    "organizationId": "991825827",
    "norwegianRegistry": "https://data.brreg.no/enhetsregisteret/api/enheter/991825827",
    "internationalRegistry": None,
    "name": "Digitaliseringsdirektoratet",
    "orgType": "ORGL",
    "orgPath": "/STAT/972417858/991825827",
    "subOrganizationOf": "972417858",
    "issued": "2007-10-15",
    "municipalityNumber": "0301",
    "industryCode": "84.110",
    "sectorCode": "6100",
    "prefLabel": {
        "nb": "Digitaliseringsdirektoratet",
        "nn": "Digitaliseringsdirektoratet",
        "en": "Norwegian Digitalisation Agency"
    },
    "allowDelegatedRegistration": None
}
org_3: dict = {
    "organizationId": "917422575",
    "norwegianRegistry": "https://data.brreg.no/enhetsregisteret/api/enheter/917422575",
    "internationalRegistry": None,
    "name": "ENTUR AS",
    "orgType": "AS",
    "orgPath": "/PRIVAT/917422575",
    "subOrganizationOf": None,
    "issued": "2016-07-04",
    "municipalityNumber": "0301",
    "industryCode": "62.010",
    "sectorCode": "1120",
    "prefLabel": None,
    "allowDelegatedRegistration": None
}
org4: dict = {
    "organizationId": "961181399",
    "norwegianRegistry": "https://data.brreg.no/enhetsregisteret/api/enheter/961181399",
    "internationalRegistry": None,
    "name": "ARKIVVERKET",
    "orgType": "ORGL",
    "orgPath": "/STAT/972417866/961181399",
    "subOrganizationOf": "972417866",
    "issued": "1995-08-09",
    "municipalityNumber": "0301",
    "industryCode": "91.013",
    "sectorCode": "6100",
    "prefLabel": None,
    "allowDelegatedRegistration": None
}
default_org: dict = {
    "prefLabel": {
        "no": "BurdeSkjerpeSeg"
    },
    "orgPath": f"/ANNET/BurdeSkjerpeSeg"
}
org_5: dict = {
    "organizationId": "915429785",
    "norwegianRegistry": "https://data.brreg.no/enhetsregisteret/api/enheter/915429785",
    "internationalRegistry": None,
    "name": "POLITI- OG LENSMANNSETATEN",
    "orgType": "ORGL",
    "orgPath": "/STAT/972417831/915429785",
    "subOrganizationOf": "972417831",
    "issued": "2015-05-22",
    "municipalityNumber": "0301",
    "industryCode": "84.240",
    "sectorCode": "6100",
    "prefLabel": {
        "no": "POLITI- OG LENSMANNSETATEN"
    },
    "allowDelegatedRegistration": None
}
org_5_without_prefLabel_object = {
    "organizationId": "915429785",
    "norwegianRegistry": "https://data.brreg.no/enhetsregisteret/api/enheter/915429785",
    "internationalRegistry": None,
    "name": "POLITI- OG LENSMANNSETATEN",
    "orgType": "ORGL",
    "orgPath": "/STAT/972417831/915429785",
    "subOrganizationOf": "972417831",
    "issued": "2015-05-22",
    "municipalityNumber": "0301",
    "industryCode": "84.240",
    "sectorCode": "6100",
    "allowDelegatedRegistration": None
}
org_alt_registry: dict = {
    "organizationId": "974760673",
    "norwegianRegistry": "https://otherreg/4760673",
    "internationalRegistry": None,
    "name": "REGISTERENHETEN I BRØNNØYSUND",
    "orgType": "ORGL",
    "orgPath": "/STAT/912660680/974760673",
    "subOrganizationOf": "912660680",
    "issued": "1995-08-09",
    "municipalityNumber": "1813",
    "industryCode": "84.110",
    "sectorCode": "6100",
    "prefLabel": None,
    "allowDelegatedRegistration": None
}
concept_es_response_size_2_total_10 = {
    "_embedded": {
        "concepts": [
            {
                "id": "13dbd4a3-4aff-498c-abdd-61d8f7d6fc40",
                "prefLabel": {
                    "nb": "pantedokument"
                },
                "publisher": {
                    "uri": "http://data.brreg.no/enhetsregisteret/enhet/974760673",
                    "name": "REGISTERENHETEN I BRØNNØYSUND",
                    "orgPath": "/STAT/912660680/974760673",
                    "prefLabel": {
                        "no": "REGISTERENHETEN I BRØNNØYSUND"
                    }
                }
            },
            {
                "id": "de5b25ad-521f-4fbd-af51-7486129c6a6f",
                "prefLabel": {
                    "nb": "kontaktinformasjon"
                },
                "publisher": {
                    "uri": "http://data.brreg.no/enhetsregisteret/enhet/9967",
                    "name": "REGISTERENHETEN I KRISTIANSUND",
                    "orgPath": "/STAT/912660680/974760673",
                    "prefLabel": {
                        "no": "REGISTERENHETEN I BRØNNØYSUND"
                    }
                }
            }
        ]
    },
    "page": {
        "size": 2,
        "totalElements": 10,
        "totalPages": 5,
        "number": 0
    }
}
info_es_response_size_1_total_7 = {
    "_embedded": {
        "informationmodels": [
            {
                "title": {},
                "publisher": {
                    "uri": "https://data.brreg.no/enhetsregisteret/api/enheter/971203420",
                    "name": "FISKERIDIREKTORATET",
                    "orgPath": "/STAT/912660680/971203420"
                }
            }

        ]

    },
    "page": {
        "size": 1,
        "totalElements": 7,
        "totalPages": 5,
        "number": 0
    }
}
dataservice_es_response_size_1_total_21 = {
    "total": 21,
    "hits": [
        {
            "nationalComponent": "true",
            "isOpenAccess": "true",
            "isOpenLicense": "true",
            "isFree": "true",
            "statusCode": "DEPRECATED",
            "deprecationInfoExpirationDate": "2019-11-27T23:00:00.000Z",
            "deprecationInfoReplacedWithUrl": "",
            "id": "7c927741-59b5-4511-855f-54ab52f8baa0",
            "title": "Barnehagefakta",
            "publisher": {
                "id": "910258028",
                "name": "LILAND OG ERDAL REVISJON",
                "orgPath": "/ANNET/910258028"
            }
        }
    ]
}


def dataset_parsed_response(total_elements: int):
    return {"count": total_elements}


def dataset_parsed_with_iri(total_elements: int, iri: str, name: str):
    return [ParsedContent(count=total_elements, org_id=iri, name=name)]


def mock_dataset_sparql_result(organizations: list):
    limit_str = "------------------------------------------------------------------------------------------------------------------------------------------------------------------"
    content = """| uri                                                                                                 | name                                              | count |
==================================================================================================================================================================\n"""
    for row in organizations:
        content += f" {mock_dataset_sparql_row(row)}\n"
    return f"{limit_str}\n{content}{limit_str}"


def mock_dataset_sparql_row(organization):
    org_iri = organization["norwegianRegistry"]
    name = organization["name"]
    count = 77
    return f"| {org_iri} | {name} | {count}|"


geonorge_rdf_organization = """<?xml version="1.0" encoding="utf-8"?>
<rdf:RDF xmlns:skos="http://www.w3.org/2004/02/skos/core#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:adms="http://www.w3.org/ns/adms#" xmlns:dcat="http://www.w3.org/ns/dcat#" xml:base="https://register.geonorge.no/organisasjoner//1fe72a41-cac4-4f16-8dc1-beb568843537">
    <skos:ConceptScheme rdf:about="https://register.geonorge.no/organisasjoner/fylkeskommunene/1fe72a41-cac4-4f16-8dc1-beb568843537">
        <skos:prefLabel xml:lang="no">Fylkeskommunene</skos:prefLabel>
        <skos:prefLabel xml:lang="nb">Fylkeskommunene</skos:prefLabel>
        <skos:Definition>Norske fylkeskommuner</skos:Definition>
        <dcterms:description xml:lang="no">Norske fylkeskommuner</dcterms:description>
        <dcterms:identifier></dcterms:identifier>
        <adms:status>Gyldig</adms:status>
        <dcterms:source rdf:resource="https://register.geonorge.no/organisasjoner/fylkeskommunene/1fe72a41-cac4-4f16-8dc1-beb568843537" />
    </skos:ConceptScheme>
</rdf:RDF>"""

parsed_org_from_geonorge = {'name': 'Fylkeskommunene',
                            'orgPath': '/ANNET/Fylkeskommunene',
                            'organizationId': 'http://oneofthegoodones/56725740',
                            'prefLabel': {'nb': 'Fylkeskommunene', 'no': 'Fylkeskommunene'}
                            }

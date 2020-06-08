org_1: dict = {
    "organizationId": "974760673",
    "norwegianRegistry": "https://data.brreg.no/enhetsregisteret/api/enheter/974760673",
    "internationalRegistry": None,
    "name": "REGISTERENHETEN I BRØNNØYSUND",
    "orgType": "ORGL",
    "orgPath": "STAT/912660680/974760673",
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
    "orgPath": "PRIVAT/917422575",
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
    "orgPath": "STAT/972417866/961181399",
    "subOrganizationOf": "972417866",
    "issued": "1995-08-09",
    "municipalityNumber": "0301",
    "industryCode": "91.013",
    "sectorCode": "6100",
    "prefLabel": None,
    "allowDelegatedRegistration": None
}
org_5: dict = {
    "organizationId": "915429785",
    "norwegianRegistry": "https://data.brreg.no/enhetsregisteret/api/enheter/915429785",
    "internationalRegistry": None,
    "name": "POLITI- OG LENSMANNSETATEN",
    "orgType": "ORGL",
    "orgPath": "STAT/972417831/915429785",
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
    "orgPath": "STAT/972417831/915429785",
    "subOrganizationOf": "972417831",
    "issued": "2015-05-22",
    "municipalityNumber": "0301",
    "industryCode": "84.240",
    "sectorCode": "6100",
    "allowDelegatedRegistration": None
}


def concept_response(total_elements: int):
    return {
        "page": {
            "size": 10,
            "totalElements": total_elements,
            "totalPages": 9,
            "number": 0
        }
    }


def dataservice_response(total_elements: int):
    return {
        "total": total_elements
    }


def dataset_response(total_elements: int):
    return {"count": total_elements}


def info_model_response(total_elements: int):
    return {
        "page": {
            "size": 10,
            "totalElements": total_elements,
            "totalPages": 9,
            "number": 0
        }
    }

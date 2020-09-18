from src.result_readers import OrganizationReferencesObject

org_brreg: dict = {
    "organizationId": "974760673",
    "norwegianRegistry": "https://data.brreg.no/enhetsregisteret/api/enheter/974760673",
    "internationalRegistry": None,
    "name": "REGISTERENHETEN I BRØNNØYSUND",
    "orgType": "ORGL",
    "orgPath": "/STAT/912660680/974760673",
    "subOrganizationOf": "912660680",
    "prefLabel": None
}
org_digdir: dict = {
    "organizationId": "991825827",
    "norwegianRegistry": "https://data.brreg.no/enhetsregisteret/api/enheter/991825827",
    "internationalRegistry": None,
    "name": "Digitaliseringsdirektoratet",
    "orgType": "ORGL",
    "orgPath": "/STAT/972417858/991825827",
    "subOrganizationOf": "972417858",
    "prefLabel": {
        "nb": "Digitaliseringsdirektoratet",
        "nn": "Digitaliseringsdirektoratet",
        "en": "Norwegian Digitalisation Agency"
    },
}

org_politi: dict = {
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
concept_es_response = {
    "_embedded": {
        "concepts": []
    },
    "page": {
        "size": 10,
        "totalElements": 4257,
        "totalPages": 426,
        "number": 0
    },
    "aggregations": {
        "orgPath": {
            "buckets": [
                {
                    "key": "/STAT",
                    "count": 4214
                },
                {
                    "key": "/STAT/972417807",
                    "count": 3385
                },
                {
                    "key": "/STAT/972417807/974761076",
                    "count": 3385
                },
                {
                    "key": "/STAT/983887457",
                    "count": 558
                },
                {
                    "key": "/STAT/983887457/889640782",
                    "count": 558
                },
                {
                    "key": "/STAT/912660680",
                    "count": 271
                },
                {
                    "key": "/STAT/912660680/974760673",
                    "count": 271
                },
                {
                    "key": "/ANNET",
                    "count": 43
                },
                {
                    "key": "/ANNET/910298062",
                    "count": 21
                },
                {
                    "key": "/ANNET/910244132",
                    "count": 17
                },
                {
                    "key": "/ANNET/910258028",
                    "count": 5
                }
            ]
        }
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
    "aggregations": {
        "orgPath": {
            "buckets": [
                {
                    "key": "/STAT",
                    "count": 7,
                },
                {
                    "key": "/STAT/912660680",
                    "count": 7,
                },
                {
                    "key": "/STAT/912660680",
                    "count": 7,
                }
            ]
        }
    },
    "page": {
        "size": 1,
        "totalElements": 7,
        "totalPages": 5,
        "number": 0
    }
}

parsed_kartverket_from_org_catalog = OrganizationReferencesObject.from_organization_catalog_single_response(
    {
        "organizationId": "971040238",
        "norwegianRegistry": "https://data.brreg.no/enhetsregisteret/api/enheter/971040238",
        "name": "STATENS KARTVERK",
        "orgType": "ORGL",
        "orgPath": "/STAT/972417858/971040238",
        "subOrganizationOf": "972417858",
        "issued": "1995-03-12",
        "municipalityNumber": "3007",
        "industryCode": "71.123",
        "sectorCode": "6100"
    }
)

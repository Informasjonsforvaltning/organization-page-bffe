import pytest

from src.result_readers import OrganizationStore, OrganizationReferencesObject, OrgPathParent
from src.utils import ServiceKey
from tests.test_data import parsed_kartverket_from_org_catalog

aas_kommune_sparql = {
    "name": {
        "type": "literal",
        "value": "Ås kommune"
    },
    "publisher": {
        "type": "uri",
        "value": "https://register.geonorge.no/organisasjoner/as-kommune/c084d983-080d-43b9-8c9a-344191a7405a"
    },
    "sameAs": {
        "type": "literal",
        "value": "http://data.brreg.no/enhetsregisteret/enhet/964948798"
    },
    "count": {
        "type": "literal",
        "datatype": "http://www.w3.org/2001/XMLSchema#integer",
        "value": "6"
    }
}
aas_kommune_sparql_without_publisher = {
    "name": {
        "type": "literal",
        "value": "Ås kommune"
    },
    "sameAs": {
        "type": "literal",
        "value": "http://data.brreg.no/enhetsregisteret/enhet/964948798"
    },
    "count": {
        "value": "497"
    }
}
aas_kommune_sparql_without_same_as = {
    "name": {
        "type": "literal",
        "value": "Ås kommune"
    },
    "publisher": {
        "type": "uri",
        "value": "https://register.geonorge.no/organisasjoner/as-kommune/c084d983-080d-43b9-8c9a-344191a7405a"
    },
    "count": {
        "type": "literal",
        "datatype": "http://www.w3.org/2001/XMLSchema#integer",
        "value": "6"
    }
}
aas_kommune_organization_catalog = {
    "organizationId": "964948798",
    "norwegianRegistry": "https://data.brreg.no/enhetsregisteret/api/enheter/964948798",
    "name": "ÅS KOMMUNE",
    "orgType": "KOMM",
    "orgPath": "/KOMMUNE/964948798",
    "issued": "1995-06-07",
    "municipalityNumber": "3021",
    "industryCode": "84.110",
    "sectorCode": "6500",
}
sparql_result_list = {
    "head": {
        "vars": [
            "name",
            "publisher",
            "sameAs"
        ]
    },
    "results": {
        "bindings": [
            {
                "name": {
                    "type": "literal",
                    "value": "Ås kommune"
                },
                "publisher": {
                    "type": "uri",
                    "value": "https://register.geonorge.no/organisasjoner/as-kommune/c084d983-080d-43b9-8c9a-344191a7405a"
                },
                "sameAs": {
                    "type": "literal",
                    "value": "http://data.brreg.no/enhetsregisteret/enhet/964948798"
                },
                "count": {
                    "type": "literal",
                    "datatype": "http://www.w3.org/2001/XMLSchema#integer",
                    "value": "6"
                }
            },
            {
                "name": {
                    "type": "literal",
                    "value": "Avinor"
                },
                "publisher": {
                    "type": "uri",
                    "value": "https://register.geonorge.no/organisasjoner/avinor/78ec5140-39ea-4acd-a31a-09accfa9444c"
                },
                "sameAs": {
                    "type": "literal",
                    "value": "http://data.brreg.no/enhetsregisteret/enhet/985198292"
                },
                "count": {
                    "type": "literal",
                    "datatype": "http://www.w3.org/2001/XMLSchema#integer",
                    "value": "6"
                }
            },
            {
                "name": {
                    "type": "literal",
                    "value": "Fylkesmannsembetene"
                },
                "sameAs": {
                    "type": "literal",
                    "value": "http://data.brreg.no/enhetsregisteret/enhet/921627009"
                },
                "count": {
                    "type": "literal",
                    "datatype": "http://www.w3.org/2001/XMLSchema#integer",
                    "value": "6"
                }
            },
            {
                "name": {
                    "type": "literal",
                    "value": "Kystverket"
                },
                "publisher": {
                    "type": "uri",
                    "value": "https://register.geonorge.no/organisasjoner/kystverket/ceb5e459-853e-4e2f-bb22-39dc0c09cb7b"
                },
                "sameAs": {
                    "type": "literal",
                    "value": "http://data.brreg.no/enhetsregisteret/enhet/874783242"
                },
                "count": {
                    "type": "literal",
                    "datatype": "http://www.w3.org/2001/XMLSchema#integer",
                    "value": "6"
                }
            },
            {
                "name": {
                    "type": "literal",
                    "value": "Statens vegvesen"
                },
                "publisher": {
                    "type": "uri",
                    "value": "https://dataut.vegvesen.no/organization/e6d3dc7a-752e-418b-9afd-36533b370285"
                }
            },
            {
                "name": {
                    "type": "literal",
                    "value": "Norges geologiske undersøkelse"
                },
                "publisher": {
                    "type": "uri",
                    "value": "https://register.geonorge.no/organisasjoner/norges-geologiske-undersokelse/d7142a92-418e-487e-a6ff-0e32c6ae31d8"
                },
                "sameAs": {
                    "type": "literal",
                    "value": "http://data.brreg.no/enhetsregisteret/enhet/970188290"
                }
            }
        ]
    }
}
mocked_organization_catalog_response = [
    {
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
    },
    {
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
    },
    {
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
    }]


def parsed_org_catalog_mock():
    return OrganizationReferencesObject.from_organization_catalog_list_response(mocked_organization_catalog_response)


@pytest.mark.unit
def test_new_organization_store():
    store_instance: OrganizationStore = OrganizationStore.get_instance()
    store_instance.organizations = []
    store_instance.update(organizations=parsed_org_catalog_mock())
    assert len(store_instance.organizations) == 3
    result = OrganizationStore.get_instance()
    assert result == store_instance


@pytest.mark.unit
def test_org_path_parent():
    parent = OrgPathParent("/STAT/12345")

    assert parent == OrgPathParent("/STAT/12345/123489")
    assert parent != OrgPathParent("/STAT")
    assert parent != OrgPathParent("/STAT/12345")
    assert parent != OrgPathParent("/PRIVAT")


@pytest.mark.unit
def test_add_organization_parent():
    store_instance: OrganizationStore = OrganizationStore.get_instance()
    store_instance.organizations = []
    store_instance.update(organizations=parsed_org_catalog_mock())
    store_instance.add_organization(
        OrganizationReferencesObject(
            for_service=ServiceKey.ORGANIZATIONS,
            name="Parent of",
            org_uri="https/somenonese",
            org_path="/STAT/972417858"
        )
    )
    assert len(store_instance.organizations) == 3


@pytest.mark.unit
def test_organization_store_add_organization_from_organization_catalog():
    store_instance: OrganizationStore = OrganizationStore.get_instance()
    store_instance.organizations = []
    store_instance.update(organizations=parsed_org_catalog_mock())
    store_instance.add_organization(parsed_kartverket_from_org_catalog)
    assert len(store_instance.organizations) == 4


@pytest.mark.unit
def test_organization_store_add_sparql_result_org():
    store_instance: OrganizationStore = OrganizationStore.get_instance()
    store_instance.organizations = []
    store_instance.update(organizations=parsed_org_catalog_mock())
    aas_kommune = OrganizationReferencesObject.from_sparql_query_result(for_service=ServiceKey.DATA_SETS,
                                                                        organization=aas_kommune_sparql)
    store_instance.add_organization(for_service=ServiceKey.DATA_SERVICES, organization=aas_kommune)
    assert len(store_instance.organizations) == 4
    assert aas_kommune in store_instance.organizations


@pytest.mark.unit
def test_organization_store_add_sparql_dataset_result_org_with_existing_from_catalog():
    store_instance: OrganizationStore = OrganizationStore.get_instance()
    store_instance.organizations = []
    store_instance.update(organizations=parsed_org_catalog_mock())
    sparql_digitaliserings_direktoratet = OrganizationReferencesObject.from_sparql_query_result(
        for_service=ServiceKey.DATA_SETS,
        organization=
        {
            "name": {
                "type": "literal",
                "value": "Digitaliseringsdir"
            },
            "publisher": {
                "type": "uri",
                "value": "https://data.brreg.no/enhetsregisteret/api/enheter/991825827"
            },
            "count": {
                "value": 99
            }
        })
    store_instance.add_organization(organization=sparql_digitaliserings_direktoratet, for_service=ServiceKey.DATA_SETS)
    assert len(store_instance.organizations) == 3
    assert sparql_digitaliserings_direktoratet in store_instance.organizations
    assert store_instance.get_organization(sparql_digitaliserings_direktoratet).dataset_count == 99


@pytest.mark.unit
def test_organization_store_add_sparql_dataservices_result_org_with_existing_from_catalog():
    store_instance: OrganizationStore = OrganizationStore.get_instance()
    store_instance.organizations = []
    store_instance.update(organizations=parsed_org_catalog_mock())
    sparql_digitaliserings_direktoratet = OrganizationReferencesObject.from_sparql_query_result(
        for_service=ServiceKey.DATA_SERVICES,
        organization=
        {
            "name": {
                "type": "literal",
                "value": "Digitaliseringsdir"
            },
            "publisher": {
                "type": "uri",
                "value": "https://data.brreg.no/enhetsregisteret/api/enheter/991825827"
            },
            "count": {
                "value": 201
            }
        })
    store_instance.add_organization(organization=sparql_digitaliserings_direktoratet,
                                    for_service=ServiceKey.DATA_SERVICES)
    assert len(store_instance.organizations) == 3
    assert sparql_digitaliserings_direktoratet in store_instance.organizations
    assert store_instance.get_organization(sparql_digitaliserings_direktoratet).dataservice_count == 201


@pytest.mark.unit
def test_organization_store_add_sparql_result_org_with_same_as_in_existing_from_catalog():
    store_instance: OrganizationStore = OrganizationStore.get_instance()
    store_instance.organizations = []
    store_instance.update(organizations=parsed_org_catalog_mock())
    sparql_digitaliserings_direktoratet = OrganizationReferencesObject.from_sparql_query_result(
        for_service=ServiceKey.DATA_SETS,
        organization={
            "name": {
                "type": "literal",
                "value": "Digitaliseringsdir"
            },
            "publisher": {
                "type": "uri",
                "value": "https://register.geonorge.no/organisasjoner/as-kommune/c084d983-080d-43b9-8c9a-344191a7405a"
            },
            "sameAs": {
                "type": "uri",
                "value": "https://data.brreg.no/enhetsregisteret/api/enheter/991825827"
            },
            "count": {
                "value": "209"
            }
        })
    store_instance.add_organization(for_service=ServiceKey.DATA_SETS,
                                    organization=sparql_digitaliserings_direktoratet)
    assert len(store_instance.organizations) == 3
    assert sparql_digitaliserings_direktoratet in store_instance.organizations
    result_org = store_instance.get_organization(sparql_digitaliserings_direktoratet)
    assert result_org.org_uri == "https://data.brreg.no/enhetsregisteret/api/enheter/991825827"
    assert result_org.name == "Digitaliseringsdirektoratet"
    assert result_org.dataset_count == 209
    assert len(result_org.same_as) == 1
    assert "https://register.geonorge.no/organisasjoner/as-kommune/c084d983-080d-43b9-8c9a-344191a7405a" in result_org.same_as
    result_by_orgpath = store_instance.get_organization("/STAT/972417858/991825827")
    assert result_by_orgpath == sparql_digitaliserings_direktoratet
    assert result_by_orgpath.dataset_count == 209


@pytest.mark.unit
def test_organization_store_add_concept_to_existing_org():
    store_instance: OrganizationStore = OrganizationStore.get_instance()
    store_instance.organizations = []
    store_instance.update(organizations=parsed_org_catalog_mock())
    sparql_digitaliserings_direktoratet = OrganizationReferencesObject.from_sparql_query_result(
        for_service=ServiceKey.DATA_SETS,
        organization={
            "name": {
                "type": "literal",
                "value": "Digitaliseringsdir"
            },
            "publisher": {
                "type": "uri",
                "value": "https://register.geonorge.no/organisasjoner/as-kommune/c084d983-080d-43b9-8c9a-344191a7405a"
            },
            "sameAs": {
                "type": "uri",
                "value": "https://data.brreg.no/enhetsregisteret/api/enheter/991825827"
            },
            "count": {
                "value": "358"
            }
        })
    store_instance.add_organization(for_service=ServiceKey.DATA_SETS,
                                    organization=sparql_digitaliserings_direktoratet)
    brreg_concepts = {
        "key": "/STAT/972417858/991825827",
        "count": 66
    }
    store_instance.add_organization(
        for_service=ServiceKey.CONCEPTS,
        organization=
        OrganizationReferencesObject.from_es_response(
            for_service=ServiceKey.CONCEPTS,
            es_response=brreg_concepts
        )
    )

    assert len(store_instance.organizations) == 3
    assert "/STAT/972417858/991825827" in store_instance.organizations
    result_org = store_instance.get_organization(sparql_digitaliserings_direktoratet)
    assert len(result_org.same_as) == 1
    assert result_org.name == "Digitaliseringsdirektoratet"
    assert result_org.dataset_count == 358
    assert result_org.concept_count == 66


@pytest.mark.unit
def test_content_from_all_content_types():
    store_instance: OrganizationStore = OrganizationStore.get_instance()
    store_instance.organizations = []
    store_instance.update(organizations=parsed_org_catalog_mock())
    sparql_digir_datasets = OrganizationReferencesObject.from_sparql_query_result(
        for_service=ServiceKey.DATA_SETS,
        organization={
            "name": {
                "type": "literal",
                "value": "Digitaliseringsdir"
            },
            "publisher": {
                "type": "uri",
                "value": "https://register.geonorge.no/organisasjoner/as-kommune/c084d983-080d-43b9-8c9a-344191a7405a"
            },
            "sameAs": {
                "type": "uri",
                "value": "https://data.brreg.no/enhetsregisteret/api/enheter/991825827"
            },
            "count": {
                "value": "358"
            }
        })
    sparql_digir_dataservices = OrganizationReferencesObject.from_sparql_query_result(
        for_service=ServiceKey.DATA_SERVICES,
        organization={
            "sameAs": {
                "type": "uri",
                "value": "https://data.brreg.no/enhetsregisteret/api/enheter/991825827"
            },
            "count": {
                "value": "206"
            }
        })
    store_instance.add_organization(for_service=ServiceKey.DATA_SETS,
                                    organization=sparql_digir_datasets)
    store_instance.add_organization(for_service=ServiceKey.DATA_SERVICES,
                                    organization=sparql_digir_dataservices)
    brreg_concepts = {
        "key": "/STAT/972417858/991825827",
        "count": 66
    }
    informationmodel_concepts = {
        "key": "/STAT/972417858/991825827",
        "count": 755
    }
    store_instance.add_organization(
        for_service=ServiceKey.CONCEPTS,
        organization=
        OrganizationReferencesObject.from_es_response(
            for_service=ServiceKey.CONCEPTS,
            es_response=brreg_concepts
        )
    )
    store_instance.add_organization(
        for_service=ServiceKey.INFO_MODELS,
        organization=
        OrganizationReferencesObject.from_es_response(
            for_service=ServiceKey.INFO_MODELS,
            es_response=informationmodel_concepts
        )
    )

    assert len(store_instance.organizations) == 3
    result = store_instance.get_organization(sparql_digir_dataservices)
    assert result.informationmodel_count == 755
    assert result.concept_count == 66
    assert result.dataservice_count == 206
    assert result.dataset_count == 358


@pytest.mark.unit
def test_sparql_references_parser():
    result = OrganizationReferencesObject.from_sparql_query_result(ServiceKey.DATA_SETS, aas_kommune_sparql)
    assert result.name == "Ås kommune"
    assert len(result.same_as) == 1
    assert result.org_uri == "http://data.brreg.no/enhetsregisteret/enhet/964948798"
    assert result.same_as[0] == "https://register.geonorge.no/organisasjoner/as-kommune/c084d983-080d-43b9-8c9a" \
                                "-344191a7405a"
    assert result.dataset_count == 6


@pytest.mark.unit
def test_sparql_references_parser_without_same_as():
    data = {
        "name": {
            "type": "literal",
            "value": "Ås kommune"
        },
        "publisher": {
            "type": "uri",
            "value": "https://register.geonorge.no/organisasjoner/as-kommune/c084d983-080d-43b9-8c9a-344191a7405a"
        },
        "count": {
            "value": "10"
        }
    }
    result = OrganizationReferencesObject.from_sparql_query_result(for_service=ServiceKey.DATA_SERVICES,
                                                                   organization=data)
    assert result.name == "Ås kommune"
    assert len(result.same_as) == 1
    assert result.same_as[0] == "https://register.geonorge.no/organisasjoner/as-kommune/c084d983-080d-43b9-8c9a" \
                                "-344191a7405a"
    assert result.org_uri is None
    assert result.dataservice_count == 10


@pytest.mark.unit
def test_sparql_references_parser_without_publisher():
    data = {
        "name": {
            "type": "literal",
            "value": "Ås kommune"
        },
        "sameAs": {
            "type": "literal",
            "value": "http://data.brreg.no/enhetsregisteret/enhet/964948798"
        },
        "count": {
            "value": 6
        }
    }
    expected = OrganizationReferencesObject.from_sparql_query_result(for_service=ServiceKey.DATA_SERVICES,
                                                                     organization=data)
    assert expected.name == "Ås kommune"
    assert len(expected.same_as) == 0
    assert expected.org_uri == "http://data.brreg.no/enhetsregisteret/enhet/964948798"


@pytest.mark.unit
def test_sparql_references_parser_without_publisher():
    data = {
        "name": {
            "type": "literal",
            "value": "Ås kommune"
        },
        "sameAs": {
            "type": "literal",
            "value": "http://data.brreg.no/enhetsregisteret/enhet/964948798"
        },
        "count": {
            "value": 6
        }
    }
    expected = OrganizationReferencesObject.from_sparql_query_result(for_service=ServiceKey.DATA_SETS,
                                                                     organization=data)
    assert expected.name == "Ås kommune"
    assert len(expected.same_as) == 0
    assert expected.org_uri == "http://data.brreg.no/enhetsregisteret/enhet/964948798"


@pytest.mark.unit
def test_parse_from_organization_catalog_json():
    data = {
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

    result = OrganizationReferencesObject.from_organization_catalog_single_response(data)
    assert result.org_uri == "https://data.brreg.no/enhetsregisteret/api/enheter/991825827"
    assert len(result.same_as) == 0
    assert result.org_path == "/STAT/972417858/991825827"
    assert result.name == "Digitaliseringsdirektoratet"
    assert result.dataset_count == 0
    assert result.dataservice_count == 0
    assert result.informationmodel_count == 0
    assert result.concept_count == 0


@pytest.mark.unit
def test_parse_from_concept_harvester_response():
    response = {
        "key": "/STAT/972417807/974761076",
        "count": 3402
    }

    result = OrganizationReferencesObject.from_es_response(for_service=ServiceKey.CONCEPTS,
                                                           es_response=response
                                                           )
    assert result.org_path == response["key"]
    assert result.concept_count == 3402
    assert result.informationmodel_count == 0
    assert result.dataset_count == 0
    assert result.dataservice_count == 0
    assert result.name is None
    assert len(result.same_as) == 0
    assert result.org_uri is None
    assert result.name is None


@pytest.mark.unit
def test_parse_from_informationmodel_harvester_response():
    response = {
        "key": "/STAT/972417807/974761076",
        "count": 68
    }

    result = OrganizationReferencesObject.from_es_response(for_service=ServiceKey.INFO_MODELS,
                                                           es_response=response
                                                           )
    assert result.org_path == response["key"]
    assert result.concept_count == 0
    assert result.informationmodel_count == 68
    assert result.dataset_count == 0
    assert result.dataservice_count == 0
    assert result.name is None
    assert len(result.same_as) == 0
    assert result.org_uri is None
    assert result.name is None


@pytest.mark.unit
def test_eq_on_org_uri():
    from_sparql_result = OrganizationReferencesObject.from_sparql_query_result(
        ServiceKey.DATA_SETS,
        aas_kommune_sparql
    )
    from_sparql_result_no_publisher = OrganizationReferencesObject.from_sparql_query_result(
        ServiceKey.DATA_SETS,
        aas_kommune_sparql_without_publisher
    )
    from_sparql_result_no_same_as = OrganizationReferencesObject.from_sparql_query_result(
        ServiceKey.DATA_SETS,
        aas_kommune_sparql_without_same_as
    )
    from_org_catalog_json = OrganizationReferencesObject.from_organization_catalog_single_response(
        aas_kommune_organization_catalog
    )

    assert from_sparql_result == from_org_catalog_json
    assert from_sparql_result_no_publisher == from_org_catalog_json
    assert from_sparql_result_no_same_as != from_org_catalog_json


@pytest.mark.unit
def test_eq_on_both_with_same_as_and_no_org_uri():
    same_as_with_name = OrganizationReferencesObject(
        for_service=ServiceKey.DATA_SETS,
        name="Geovekst",
        same_as_entry="https://register.geonorge.no/organisasjoner/geovekst/7ac1627a-2e25-4dad-9213-c04a15a462e4"
    )
    same_as_without_name_https = OrganizationReferencesObject(
        for_service=ServiceKey.DATA_SERVICES,
        same_as_entry="https://register.geonorge.no/organisasjoner/geovekst/7ac1627a-2e25-4dad-9213-c04a15a462e4"
    )
    same_as_without_name_no_match = OrganizationReferencesObject(
        for_service=ServiceKey.DATA_SETS,
        same_as_entry="https://register.geonorge.no/organisasjoner/geov/7ac1627a-4dad-9213-c04a15a462e4"
    )
    same_as_without_name_http = OrganizationReferencesObject(
        for_service=ServiceKey.DATA_SERVICES,
        same_as_entry="https://register.geonorge.no/organisasjoner/geovekst/7ac1627a-2e25-4dad-9213-c04a15a462e4"
    )

    assert same_as_without_name_http == same_as_with_name
    assert same_as_without_name_https == same_as_with_name
    assert same_as_without_name_no_match != same_as_with_name
    assert same_as_without_name_http == same_as_without_name_https


@pytest.mark.unit
def test_organization_from_dataservice_without_same_as_entry():
    entry = {
        "publisher": {
            "type": "uri",
            "value": "https://organization-catalogue.fellesdatakatalog.brreg.no/organizations/991825827"
        },
        "count": {
            "type": "literal",
            "datatype": "http://www.w3.org/2001/XMLSchema#integer",
            "value": "7"
        }
    }
    expected_org_uri = "https://data.brreg.no/enhetsregisteret/api/enheter/991825827"

    result = OrganizationReferencesObject.from_sparql_query_result(
        for_service=ServiceKey.DATA_SERVICES,
        organization=entry
    )

    assert result.dataservice_count == 7
    assert result.org_uri == expected_org_uri

    test_eq_object = OrganizationReferencesObject(
        name="Test Name",
        org_uri=expected_org_uri,
        for_service=ServiceKey.CONCEPTS,
        count=2354
    )

    assert result == test_eq_object


@pytest.mark.unit
def test_add_organization_from_dataservice_without_same_as_entry():
    entry = {
        "publisher": {
            "type": "uri",
            "value": "https://organization-catalogue.fellesdatakatalog.brreg.no/organizations/991825827"
        },
        "count": {
            "type": "literal",
            "datatype": "http://www.w3.org/2001/XMLSchema#integer",
            "value": "7"
        }
    }
    expected_org_uri = "https://data.brreg.no/enhetsregisteret/api/enheter/991825827"

    no_same_as_object = OrganizationReferencesObject.from_sparql_query_result(
        for_service=ServiceKey.DATA_SERVICES,
        organization=entry
    )

    test_eq_object = OrganizationReferencesObject(
        name="Test Name",
        org_uri=expected_org_uri,
        for_service=ServiceKey.CONCEPTS,
        count=2354
    )

    store = OrganizationStore.get_instance()
    store.add_organization(test_eq_object, for_service=ServiceKey.CONCEPTS)
    store.add_organization(no_same_as_object, for_service=ServiceKey.DATA_SERVICES)
    assert no_same_as_object in store.organizations
    result = store.get_organization(no_same_as_object)
    assert result.dataservice_count == 7
    assert result.concept_count == 2354


@pytest.mark.unit
def test_reduce_for_response():
    politi_ref = OrganizationReferencesObject(
        name="POLITI- OG LENSMANNSETATEN",
        org_path="/STAT/972417831/915429785",
        org_uri="https://data.brreg.no/enhetsregisteret/api/enheter/915429785",
        count=3,
        for_service=ServiceKey.DATA_SETS)
    some_other_ref = OrganizationReferencesObject(
        name="STRANDA SAG- OG HØVLERI",
        org_path="/PRIVAT/1256847",
        org_uri="https://data.brreg.no/enhetsregisteret/api/enheter/1256847",
        count=88,
        for_service=ServiceKey.CONCEPTS)
    one_empty_ref = OrganizationReferencesObject(
        name="EMPTY NONSENSE",
        org_path="/ANNET/1256847",
        for_service=ServiceKey.ORGANIZATIONS)
    politi_parent_ref = OrganizationReferencesObject(
        name="LOVER OG SÅNNE TING",
        org_path="/STAT/972417831",
        org_uri="https://data.brreg.no/enhetsregisteret/api/enheter/972417831",
        count=99,
        for_service=ServiceKey.DATA_SETS)
    politi_root_orgpath_ref = OrganizationReferencesObject(
        name="Stat",
        org_path="/STAT",
        count=99,
        for_service=ServiceKey.DATA_SETS)

    store = OrganizationStore.get_instance()
    store.organizations = []
    store.add_organization(organization=politi_parent_ref, for_service=ServiceKey.DATA_SETS)
    store.add_organization(organization=politi_ref, for_service=ServiceKey.DATA_SETS)
    store.add_organization(organization=politi_root_orgpath_ref, for_service=ServiceKey.DATA_SETS)
    store.add_organization(organization=one_empty_ref)
    store.add_organization(some_other_ref)

    result = store.get_organization_list()
    assert len(result) == 3
    result_names = [org.name for org in result]
    assert "POLITI- OG LENSMANNSETATEN" in result_names
    assert "STRANDA SAG- OG HØVLERI" in result_names
    assert "EMPTY NONSENSE" in result_names
    assert "LOVER OG SÅNNE TING" not in result_names
    assert "Stat" not in result_names


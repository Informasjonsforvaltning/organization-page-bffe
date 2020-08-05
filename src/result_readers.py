import logging
import re
from itertools import groupby
from rdflib import Graph, URIRef, SKOS


class RegistryUrls:
    NATIONAL = "data.brreg.no"
    GEO_NORGE = "register.geonorge.no"


class ParsedContent:
    def __init__(self, count: int, org_id: str, name: str):
        self.count = count
        self.name = name
        if not org_id.startswith("http"):
            self.org_id = org_id

        elif re.findall(RegistryUrls.NATIONAL, org_id):
            self.norwegianRegistry_iri = org_id
            self.org_id = self.get_norwegian_registry_id()
        else:
            if re.findall(RegistryUrls.GEO_NORGE, org_id).__len__() < 1:
                logging.error(f"organization IRI {org_id} does not belong to any known registry")
            self.alternativeRegistry_iri = org_id

    def get_norwegian_registry_id(self):
        if hasattr(self, 'norwegianRegistry_iri'):
            org_id = self.norwegianRegistry_iri.split(sep='/')
            return org_id[len(org_id) - 1]
        elif hasattr(self, 'org_id') and self.org_id[0].isdigit():
            return self.org_id
        else:
            return None

    def __eq__(self, other):
        if isinstance(other, str):
            uri_split = other.split(sep="/")
            if hasattr(self, 'org_id') and len(uri_split) > 1 and self.org_id == uri_split[len(uri_split) - 1]:
                return True
            elif hasattr(self,'org_id') and other == self.org_id:
                return True
            elif hasattr(self, 'alternativeRegistry_iri') and self.alternativeRegistry_iri == other:
                return True
            else:
                return self.name == other
        else:
            if hasattr(self, 'org_id'):
                if hasattr(other, 'org_id'):
                    return other.org_id == self.org_id
                else:
                    return False
            elif hasattr(self, 'alternativeRegistry_iri'):
                if hasattr(other, 'alternativeRegistry_iri'):
                    other_split_uri = other.alternativeRegistry_iri.split("//")
                    self_split_uri = self.alternativeRegistry_iri.split("//")
                    return other_split_uri[len(other_split_uri) - 1] == self_split_uri[len(self_split_uri) - 1]
                else:
                    return False
            elif hasattr(self, 'name'):
                if hasattr(self, 'name'):
                    return self.name == other.name
            else:
                return False

    def __hash__(self):
        if hasattr(self, 'norwegianRegistry_iri'):
            org_id = self.norwegianRegistry_iri.split(sep='/')
            return hash(org_id[org_id.__len__() - 1])
        elif hasattr(self, 'org_id'):
            return hash(self.org_id)
        else:
            return hash(self.name)


def read_sparql_table(table: str) -> list:
    content = []
    for row in table.splitlines():
        if row.startswith('-') or row.startswith("=") or row.startswith('| uri'):
            continue
        else:
            content.append(read_sparql_row(row))
    return content


def read_sparql_row(row: str) -> ParsedContent:
    iri, name, count = row.replace('"', '').split(sep='|')[1:4]
    return ParsedContent(count=int(count.strip()), org_id=iri.strip(), name=name.strip())


def parse_es_results(es_results: list, with_uri: bool):
    parsed_result = []
    if with_uri:
        results_by_uri = group_by_org_uri(es_results)
        for organization in results_by_uri:
            parsed_result.append(ParsedContent(count=organization["name"].__len__(),
                                               org_id=organization["uri"],
                                               name=organization["name"][0]))
    else:
        results_by_uri = group_by_org_id(es_results)
        for organization in results_by_uri:
            parsed_result.append(ParsedContent(count=organization["name"].__len__(),
                                               org_id=organization["id"],
                                               name=organization["name"][0]))

    return parsed_result


def group_by_org_uri(es_results):
    sanitized_result = []
    while es_results.__len__() > 0:
        es_entry = es_results.pop()
        if "publisher" in es_entry.keys() and len(es_entry["publisher"]):
            sanitized_result.append(es_entry)

    sorted_input = sorted(sanitized_result, key=lambda item: item["publisher"]["uri"])
    groups = groupby(sorted_input, key=lambda item: item["publisher"]["uri"])
    return [{'uri': k, 'name': [x["publisher"]["name"] for x in v]} for k, v in groups]


def group_by_org_id(es_results):
    sanitized_result = []
    while es_results.__len__() > 0:
        es_entry = es_results.pop()
        if "publisher" in es_entry.keys() and len(es_entry["publisher"]):
            sanitized_result.append(es_entry)
    sorted_input = sorted(sanitized_result, key=lambda item: item["publisher"]["id"])
    groups = groupby(sorted_input, key=lambda item: item["publisher"]["id"])
    return [{'id': k, 'name': [x["publisher"]["name"] for x in v]} for k, v in groups]


def read_alt_organization_rdf_xml(organization):
    graph = Graph()
    graph.parse(data=organization, format="application/rdf+xml")
    pref_label_pred = URIRef("http://www.w3.org/2004/02/skos/core#prefLabel")
    pref_labels = {}
    for pref_label in graph.objects(predicate=pref_label_pred):
        pref_labels[pref_label.language] = pref_label.value

    return {
        "prefLabel": pref_labels,
        "name": org_path_label(pref_labels),
        "orgPath": f"/ANNET/{org_path_label(pref_labels)}"
    }


def org_path_label(pref_labels: dict) -> str:
    if "no" in pref_labels.keys():
        return pref_labels["no"]
    else:
        return pref_labels.values()[0]

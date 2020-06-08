import logging
import re


class RegistryUrls:
    NATIONAL = "data.brreg.no/enhetsregisteret"
    GEO_NORGE = "register.geonorge.no"


class ParsedResult:
    def __init__(self, count: int, organizationIri: str, name: str):

        self.count = count
        if re.findall(RegistryUrls.NATIONAL, organizationIri):
            self.norwegianRegistry_iri = organizationIri
        else:
            if re.findall(RegistryUrls.GEO_NORGE, organizationIri) != 1:
                logging.error(f"organization IRI {organizationIri} does not belong to any known registry")
            self.alternativeRegistry_iri = organizationIri
            self.name = name


def read_sparql_table(table: str) -> list:
    content = []
    for row in table.splitlines():
        if row.startswith('-') or row.startswith("=") or row.startswith('| id'):
            continue
        else:
            content.append(read_sparql_row(row))
    return content


def read_sparql_row(row: str) -> ParsedResult:
    iri, name, count = row.replace('"', '').split(sep='|')[1:4]
    return ParsedResult(count=int(count.strip()), organizationIri=iri.strip(), name=name.strip())

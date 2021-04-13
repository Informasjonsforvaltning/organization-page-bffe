"""Test responses."""

ramsund = """{
  "organization": {
    "organizationId": "910244132",
    "name": "RAMSUND OG ROGNAN REVISJON",
    "prefLabel": {
      "nb": "Ramsund og Rognand revisjon"
    },
    "orgPath": "/ANNET/910244132",
    "orgType": null,
    "sectorCode": null,
    "industryCode": null,
    "homepage": null,
    "seeAlso": null,
    "icon": "https://orglogo.difi.no/api/logo/org/910244132"
  },
  "datasets": {
    "total": 70,
    "new": 3,
    "authoritative": 10,
    "open": 15,
    "quality": {
      "category": "sufficient",
      "percentage": 33
    }
  }
}"""

fiskeri = """{
  "organization": {
    "organizationId": "971203420",
    "name": "FISKERIDIREKTORATET",
    "prefLabel": {
      "nb": "Fiskeridirektoratet"
    },
    "orgPath": "/STAT/912660680/971203420",
    "orgType": "Organisasjonsledd",
    "sectorCode": "6100 Statsforvaltningen",
    "industryCode": "84.130 Offentlig administrasjon tilknyttet næringsvirksomhet og arbeidsmarked",
    "homepage": "www.fiskeridir.no/",
    "seeAlso": "https://data.brreg.no/enhetsregisteret/oppslag/enheter/971203420",
    "icon": "https://orglogo.difi.no/api/logo/org/971203420"
  },
  "datasets": {
    "total": 10,
    "new": 0,
    "authoritative": 0,
    "open": 9,
    "quality": {
      "category": "excellent",
      "percentage": 85
    }
  }
}"""

all_catalogs = """{
  "organizations": [
    {
      "id": "910258028",
      "name": "LILAND OG ERDAL REVISJON",
      "prefLabel": {
        "nb": "Liland og erdal revisjon"
      },
      "datasetCount": 20,
      "conceptCount": 0,
      "dataserviceCount": 18,
      "informationmodelCount": 0
    },
    {
      "id": "971203420",
      "name": "FISKERIDIREKTORATET",
      "prefLabel": {
        "nb": "Fiskeridirektoratet"
      },
      "datasetCount": 10,
      "conceptCount": 0,
      "dataserviceCount": 0,
      "informationmodelCount": 0
    },
    {
      "id": "910244132",
      "name": "RAMSUND OG ROGNAN REVISJON",
      "prefLabel": {
        "nb": "Ramsund og Rognand revisjon"
      },
      "datasetCount": 70,
      "conceptCount": 0,
      "dataserviceCount": 20,
      "informationmodelCount": 0
    },
    {
      "id": "555111290",
      "name": "Høgskolen for IT og arkitektur",
      "prefLabel": {
        "nb": "Høgskolen for it og arkitektur"
      },
      "datasetCount": 0,
      "conceptCount": 0,
      "dataserviceCount": 2,
      "informationmodelCount": 0
    }
  ]
}"""

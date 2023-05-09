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
    "totalCount": 71,
    "newCount": 4,
    "authoritativeCount": 10,
    "openCount": 15,
    "quality": {
      "score": 33,
      "percentage": 33
    }
  },
  "dataservices": {
    "totalCount": 20,
    "newCount": 1
  },
  "concepts": {
    "totalCount": 0,
    "newCount": 0
  },
  "informationmodels": {
    "totalCount": 0,
    "newCount": 0
  }
}"""

ramsund_with_no_quality = """{
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
    "totalCount": 71,
    "newCount": 4,
    "authoritativeCount": 10,
    "openCount": 15,
    "quality": null
  },
  "dataservices": {
    "totalCount": 20,
    "newCount": 1
  },
  "concepts": {
    "totalCount": 0,
    "newCount": 0
  },
  "informationmodels": {
    "totalCount": 0,
    "newCount": 0
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
    "totalCount": 10,
    "newCount": 0,
    "authoritativeCount": 0,
    "openCount": 9,
    "quality": {
      "score": 85,
      "percentage": 85
    }
  },
  "dataservices": {
    "totalCount": 0,
    "newCount": 0
  },
  "concepts": {
    "totalCount": 0,
    "newCount": 0
  },
  "informationmodels": {
    "totalCount": 0,
    "newCount": 0
  }
}"""

liland = """{
    "organization": null,
    "datasets": {
        "totalCount": 19,
        "newCount": 0,
        "authoritativeCount": 0,
        "openCount": 3,
        "quality": null
    },
    "dataservices": {
        "totalCount": 18,
        "newCount": 0
    },
    "concepts": {
        "totalCount": 5,
        "newCount": 0
    },
    "informationmodels": {
        "totalCount": 2,
        "newCount": 0
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
      "conceptCount": 5,
      "dataserviceCount": 18,
      "informationmodelCount": 2
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
      "datasetCount": 71,
      "conceptCount": 22,
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
    },
    {
      "id": "974767880",
      "name": "NORGES TEKNISK-NATURVITENSKAPELIGE UNIVERSITET NTNU",
      "prefLabel": {
        "nb": "Artsdatabanken"
      },
      "datasetCount": 0,
      "conceptCount": 0,
      "dataserviceCount": 1,
      "informationmodelCount": 0
    }
  ]
}
"""

ramsund_nap = """{
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
    "totalCount": 7,
    "newCount": 0,
    "authoritativeCount": 2,
    "openCount": 2,
    "quality": {
      "score": 33,
      "percentage": 33
    }
  },
  "dataservices": {
    "totalCount": 0,
    "newCount": 0
  },
  "concepts": {
    "totalCount": 0,
    "newCount": 0
  },
  "informationmodels": {
    "totalCount": 0,
    "newCount": 0
  }
}"""

ntnu = """{
  "organization": {
    "organizationId": "974767880",
    "name": "NORGES TEKNISK-NATURVITENSKAPELIGE UNIVERSITET NTNU",
    "orgType": null,
    "orgPath": "/STAT/872417842/974767880",
    "icon": "https://orglogo.difi.no/api/logo/org/974767880",
    "industryCode": null,
    "homepage": null,
    "seeAlso": null,
    "sectorCode": null,
    "prefLabel": {
        "nb": "Artsdatabanken"
    }
  },
  "datasets": {
    "totalCount": 0,
    "newCount": 0,
    "authoritativeCount": 0,
    "openCount": 0,
    "quality": null
  },
  "dataservices": {
    "totalCount": 0,
    "newCount": 0
  },
  "concepts": {
    "totalCount": 5,
    "newCount": 0
  },
  "informationmodels": {
    "totalCount": 0,
    "newCount": 0
  }
}"""

all_nap = """{
  "organizations": [
    {
      "id": "910244132",
      "name": "RAMSUND OG ROGNAN REVISJON",
      "prefLabel": {
        "nb": "Ramsund og Rognand revisjon"
      },
      "datasetCount": 7,
      "conceptCount": 0,
      "dataserviceCount": 0,
      "informationmodelCount": 0
    },
    {
      "id": "910258028",
      "name": "LILAND OG ERDAL REVISJON",
      "prefLabel": {
        "nb": "Liland og erdal revisjon"
      },
      "datasetCount": 3,
      "conceptCount": 0,
      "dataserviceCount": 0,
      "informationmodelCount": 0
    },
    {
      "id": "971032081",
      "name": "STATENS VEGVESEN",
      "prefLabel": {
        "nb": "Statens Vegvesen"
      },
      "datasetCount": 21,
      "conceptCount": 0,
      "dataserviceCount": 0,
      "informationmodelCount": 0
    }
  ]
}"""

karmsund = """{
    "organization": {
        "organizationId": "910298062",
        "name": "KARMSUND OG KYSNESSTRAND REVISJON",
        "prefLabel": {
            "nb": "Karmsund og kysnesstrand revisjon"
        },
        "orgPath": "/ANNET/910298062",
        "orgType": null,
        "sectorCode": null,
        "industryCode": null,
        "homepage": null,
        "seeAlso": null,
        "icon": "https://orglogo.difi.no/api/logo/org/910298062"
    },
    "datasets": {
        "totalCount": 0,
        "newCount": 0,
        "authoritativeCount": 0,
        "openCount": 0,
        "quality": null
    },
    "dataservices": {
        "totalCount": 0,
        "newCount": 0
    },
    "concepts": {
        "totalCount": 0,
        "newCount": 0
    },
    "informationmodels": {
        "totalCount": 0,
        "newCount": 0
    }
}"""

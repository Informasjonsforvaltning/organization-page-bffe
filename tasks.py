import os
import requests
from invoke import task

pipenv_install = "pipenv install --dev"
root_dir = os.path


@task
def unit_test(ctx, install=False):
    pipenv_run_test = "pipenv run pytest -m unit --disable-warnings"
    if install:
        ctx.run(pipenv_install)
    ctx.run(pipenv_run_test)


@task
def build_image(ctx, tags="digdir/fdk-organization-bff:latest", staging=False):
    if staging:
        ctx.run(pipenv_install)
    gen_requirements = "pipenv lock -r >requirements.txt"
    ctx.run(gen_requirements)
    tag = ""
    for t in tags.split(","):
        tag = tag + ' -t ' + t

    print("building image with tag " + tag)
    build_cmd = "docker build . " + tag
    ctx.run(build_cmd)


# start docker-compose for contract-tests
@task
def start_docker(ctx, image="digdir/fdk-organization-bff:latest", attach=False):
    print("starting docker network..")
    host_dir = os.getcwd()
    if attach:
        start_compose = "TEST_IMAGE={0} MOCK_DIR={1} docker-compose -f  tests/docker-compose.contract.yml up".format(
            image, host_dir)
    else:
        start_compose = "TEST_IMAGE={0} MOCK_DIR={1} docker-compose -f  tests/docker-compose.contract.yml up -d".format(
            image, host_dir)
    ctx.run(start_compose)


# stop docker-compose for contract-tests
@task
def stop_docker(ctx, clean=False, remove=False):
    print("stopping docker network..")
    kill = "docker-compose -f tests/docker-compose.contract.yml kill"
    docker_clean = "docker system prune"
    ctx.run(kill)
    if remove:
        ctx.run(f"{docker_clean} -a")
    elif clean:
        ctx.run(docker_clean)


@task
def contract_test(ctx, image="digdir/fdk-organization-bff:latest", compose=False, build=False):
    print("______CONTRACT TESTS_______")
    if build:
        build_image(ctx, image)
    if compose:
        start_docker(ctx, image)
    pipenv_run_test = "pipenv run pytest -m contract --tb=line"
    ctx.run(pipenv_run_test)


@task
def update_mock_data(ctx):
    mock_url = "http://localhost:8080"
    old_harvesters_url = "https://www.fellesdatakatalog.digdir.no/api"
    org_catalog_url = "https://organization-catalogue.fellesdatakatalog.digdir.no/organizations/"
    dataset_sparql = """PREFIX dct: <http://purl.org/dc/terms/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX owl: <http://www.w3.org/2002/07/owl%23>
    SELECT ?uri ?name (COUNT(?item) AS ?count)
    WHERE {
  ?publisher a foaf:Agent .
  ?item dct:publisher ?publisher .
  {
    SELECT ?publisher ?uri ?name
    WHERE {
      ?publisher a foaf:Agent .
      OPTIONAL {
        ?publisher foaf:name ?name .
      }
      OPTIONAL {
        ?publisher owl:sameAs ?sameAs .
      }
      BIND(COALESCE(?sameAs, STR(?publisher)) AS ?uri)
    }
  }
}
GROUP BY ?uri ?name
ORDER BY DESC(?count)"""
    stop_recording_curl = "curl -I -X POST  http://localhost:8080/__admin/recordings/stop"

    data_services_curl = f"curl -I -X GET {mock_url}/apis?size=0aggregations=formats,orgPath,firstHarvested,publisher," \
                         f"openAccess,openLicence,freeUsage -H 'Accept: application/json'"

    info_models_curl = f" curl -I -X GET {mock_url}/informationmodels?aggregations=orgPath"

    ctx.run("docker-compose up -d")
    breakpoint()
    # get content from old harvesters
    start_recording_curl(record_url=old_harvesters_url)
    # concepts
    for i in range(0, 4):
        concepts_curl = f"curl -I -X GET {0}/concepts?size=5000&returnfields=publisher&page={1}".format(mock_url, i)
        ctx.run(concepts_curl)
        concepts_curl = f"curl -I -X GET {0}/concepts?size=5000&returnfields=publisher".format(mock_url, i)

    # informationmodels

    ctx.run(stop_recording_curl)
    breakpoint()
    ctx.run("docker-compose down")


def start_recording_curl(ctx, record_url):
    start_recording_req = "curl -d '{\"targetBaseUrl\": \"{0}\" }' -H " \
                          "'Content-Type: application/json' http://localhost:8080/__admin/recordings/start".format(
        record_url)
    breakpoint()
    ctx.run(start_recording_req)

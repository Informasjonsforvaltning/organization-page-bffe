fdk-fulltext-search
---------------------

## Developing
### Setup
```
% pip install pipenv    # package management tool
% pip install invoke    # a task execution tool & library
% pip install pytest    # test framework
% pipenv install --dev  # install packages from Pipfile including dev
```

#### Env variables:
```
ORGANIZATION_CATALOG_URL="http://localhost:8080/"
CONCEPT_HARVESTER_URL="http://localhost:8080/"
DATASETT_HARVESTER_URL="http://localhost:8080/"                
DATASERVICE_HARVESTER_URL="http://localhost:8080/"                 
```

```
% docker-comopose up -d                             # start mockserver
% pipenv shell                                      # open a session in the virtual environment
% FLASK_APP=src FLASK_ENV=development flask run     # run application
```
## Testing
### Running tests
```
% invoke unit-test
options:
--install: install pip-dependencies, used by github actions
```
```
% invoke contract-test 
options:
--build: build image for testing before run
--compose: start docker compose for testing before run
--image: name of the image that should be tested. Defaults to digdir/fulltext-search:latest
```
#### Updating mock data
1. Set API_URL env variable to the url you want to collect mock data from
2. Start a wiremock instance 
3. Start [record and playback](http://wiremock.org/docs/record-playback/) with target url 
3. run the wanted http requests 
4. copy files from the wiremock instance's /mappings directory into mock/mappings

### Other invoke tasks
```
build-image                 # build docker image
options:
--tags                      # commaseperated list of tags for image        
```

```
stop-docker        #shut down containers used in contracttests
options:
--clean                      #remove associated containers and networks
--remove                     #remove associated containers, networks and images   
```
 
 
## Troubleshooting
### Mac: unknown locale: UTF-8 in Python
`open ~/.bash_profile:`

```
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
```
restart terminal
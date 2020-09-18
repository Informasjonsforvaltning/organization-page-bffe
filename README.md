fdk-organization-bff
---------------------
Backend-for-frontend service that provides content for fdk portal's organization pages. 

## Developing
### Setup
#### python tools 
```
% pip install pipenv    # package management tool
% pip install invoke    # a task execution tool & library
```

#### virtual environment
```
% pipenv install --dev  # install packages from Pipfile including dev
```

#### Env variables:
```          
ORGANIZATION_CATALOG_URL=http://localhost:8080/organizations
CONCEPT_HARVESTER_URL=http://localhost:8080/concepts
DATASET_HARVESTER_URL=http://localhost:8080/datasets
INFORMATIONMODELS_HARVESTER_URL=http://localhost:8080/informationmodels
DATASERVICE_HARVESTER_URL=http://localhost:8080/dataservices
FDK_BASE=http://localhost:8080
METADATA_QUALITY_ASSESSMENT_SERVICE_HOST=http://localhost:8080/assessment
SEARCH_FULLTEXT_HOST=http://localhost:8080/search
```
### Running the application 
#### in commandline 

```
% docker-comopose up -d                             # start mockserver
% pipenv shell                                      # open a session in the virtual environment
% FLASK_APP=src FLASK_ENV=development flask run     # run application
```


#### in pycharm
1. Get location of the project's virtual environment
    1. run `pipenv shell` in commandline
    2. copy the file path output located in the third line of output from the command 
    3. Remove last path fragment `/activate`
2. Pycharm configuration
    1. Run -> Edit configuration
    2. Choose Python template
    3. Template values:
        * Name: run flask
        * Script path: <file_path_to_virual_envrionment>/flask
        * Parameters: run
        * Environment variables: PYTHONBUFFERED=1;FLASK_APP=src
    4. Press OK
    5. Choose "run flask" in the drop down menu located in the upper left corner
    6. Start mock server : `% docker-comopose up -d`
    7. Run application


### *Note*
*The first time you run the application, it might take some time before the port is available due to an
update of data in elasticsearch*    

###Task automation
A number of repeating tasks are automated for convenience using [Invoke](http://www.pyinvoke.org/). (See section "Invoke tasks" for more info)

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
--image: name of the image that should be tested. Defaults to digdir/reports-bff:latest
```


### Invoke tasks
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
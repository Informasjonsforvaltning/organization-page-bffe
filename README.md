fdk-organization-bff
---------------------
Backend-for-frontend service that provides content for fdk portal's organization pages. 

## Develop and run locally
### Requirements
- [poetry](https://python-poetry.org/)
- [nox](https://nox.thea.codes/en/stable/)
- [nox-poetry](https://pypi.org/project/nox-poetry/)

### Install software:
```
% pip install poetry==1.7.1
% pip install nox==2023.4.22
% pip install nox-poetry==1.0.3
% poetry install
```

#### Env variables:
```
ORGANIZATION_CATALOG_URI
DATA_BRREG_URI
FDK_PORTAL_URI
FDK_METADATA_QUALITY_URI
```
### Running the application 
#### in commandline
```
% poetry shell
% gunicorn --chdir src "fdk_organization_bff:create_app" --config=src/fdk_organization_bff/gunicorn_config.py --worker-class aiohttp.GunicornWebWorker
```

#### with docker-compose
```
% docker-compose up -d --build
```

## Testing
### Running tests
#### with nox sessions
Run default sessions:
```
% nox
```

Run specific session:
```
% nox -s black
% nox -s unit_tests
```

#### outside nox sessions
```
% poetry run pytest
```

## Updating mock data

1. Set API_URL env variable to `http://0.0.0.0:8000`
2. Start wiremock with `docker-compose up`
2. Go to `http://0.0.0.0:8000/__admin/recorder/` and start recording with target url 
3. Send request to capture
4. Stop recording
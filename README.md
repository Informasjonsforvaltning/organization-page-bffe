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
% pip install poetry==1.1.4
% pip install nox==2020.12.31
% pip install nox-poetry==0.8.4
% poetry install
```

#### Env variables:
```
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

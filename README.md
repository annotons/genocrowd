# Genocrowd

[![Lint and test](https://github.com/annotons/genocrowd/workflows/Lint%20and%20test/badge.svg)](https://github.com/annotons/genocrowd/actions)
[![Docker Build](https://img.shields.io/docker/pulls/annotons/genocrowd.svg)](https://hub.docker.com/r/annotons/genocrowd/)
[![Documentation Status](https://readthedocs.org/projects/genocrowd/badge/?version=latest)](https://genocrowd.readthedocs.io/en/latest/?badge=latest)

![genocrowd logo](genocrowd/static/logo/logoGenocrowd.png)

Genocrowd is a web app aiming to ease manual genome annotation curation by citizens.

It is still under heavy development.

# Documentation

All documentation, included installation instruction will be [here](https://genocrowd.readthedocs.io/en/latest/) when it's written

# Running it with Docker

```
docker-compose build
docker-compose -f docker-compose.prod.yml up -d
```

Browse to http://localhost:5555/

To run in dev mode (code auto reload, non-minified js), use the corresponding docker-compose config:

```
docker-compose up -d
```

# Running tests

Run the app with docker-compose, then run this:

```
docker-compose exec genocrowd pytest
```

If you need more details and debug logs:

```
docker-compose exec genocrowd pytest -v --log-cli-level debug
```

To run some specific tests:

```
docker-compose exec genocrowd pytest -v --log-cli-level debug tests/test_api.py
docker-compose exec genocrowd pytest -v --log-cli-level debug tests/test_api.py -k test_start
```

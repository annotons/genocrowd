# Running it with Docker

In production, Genocrowd is deployed with docker and docker-compose. We provide `docker-compose.yml` templates to deploy your instance.

## Production mode

First, if running in production, make sure to change default password and secret keys in `./docker/genocrowd.ini` and `docker-compose.prod.yml`.

Then run all containers like this (using the specific production docker-compose file):

```
docker-compose -f docker-compose.prod.yml up -d
```

Browse to http://localhost:9100/

## Development mode

To run in dev mode (code auto reload, non-minified js), you need to build the Docker image:

```
docker-compose build
```

And then run all containers like this:

```
docker-compose up -d
```

Browse to http://localhost:9100/

Genocrowd continuous integration is composed of code linting and unit tests on the Python API. CI is launched automaticaly on the [genocrowd](https://github.com/annotons/genocrowd) repository on every pull requests. No PR will be merged if the CI fail.


# Setup CI environment

Genocrowd CI need a clean environment. To get it, use `ci/docker-compose.yml` of [genocrowd-docker-compose](https://github.com/annotons/genocrowd-docker-compose). This file will deploy all dependencies on ports specified in `config/genocrowd.test.ini`.

```bash
git clone https://github.com/annotons/genocrowd-docker-compose
cd genocrowd-docker-compose/ci
docker-compose up -d
```

# Run CI locally

Use `test.sh` to launch the CI. The script will launch the same commands as Travis-CI.

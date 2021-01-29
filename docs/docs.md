All the documentation (including what you are reading) can be found [here](https://genocrowd.readthedocs.io). Files are on the [Genocrowd repository](https://github.com/annotons/genocrowd/tree/master/docs).

# Serve doc locally

To serve docs locally, run

```bash
cd genocrowd

# Create the genocrowd virtual env if not already existing
virtualenv .venv
. .venv/bin/activate
pip install -r docs/requirements.txt

mkdocs serve
```

Site will be available at [localhost:8000](localhost:8000)

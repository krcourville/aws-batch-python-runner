# gb-util

Utilities for working with data from [Project Gutenberg](https://www.gutenberg.org)

## Prequisite Installations

* Python: tested with 3.8
* [pyenv](https://github.com/pyenv/pyenv): highly recommended for working with
multiple versions of Python.

## Getting started

```sh
python 3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

# for development
pip install -r requirements-dev.txt

python gb-util --help
```

## References

* <https://www.gutenberg.org/ebooks/offline_catalogs.html#the-project-gutenberg-catalog-metadata-in-machine-readable-format>
* [aiohttp Client](https://us-pycon-2019-tutorial.readthedocs.io/aiohttp_client.html)
* [Python Application Layouts: A Reference](https://realpython.com/python-application-layouts)
* [Hands-on Intro to aiohttp](https://us-pycon-2019-tutorial.readthedocs.io/aiohttp_client.html)
* <https://investigate.ai/>
* <https://gmusumeci.medium.com/how-to-deploy-aws-ecs-fargate-containers-step-by-step-using-terraform-545eeac743be>

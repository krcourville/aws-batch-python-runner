# gb-util

Utilities for working with data from [Project Gutenberg](https://www.gutenberg.org)

## Prerequisite Installations

* Python: tested with 3.8
* [pyenv](https://github.com/pyenv/pyenv): highly recommended for working with
multiple versions of Python.
* Terraform

## Getting started

### Deploying the Infrastructure

```sh
pushd infrastructure
terraform init
terraform import aws_cloudwatch_log_group.aws_batch_job_log_group /aws/batch/job
popd
```

### Running the cli

```sh
pushd src
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

# for development
pip install -r requirements-dev.txt

python gb-util.py --help
```

### Docker

```sh
# build the image
docker build ./src -f ./src/Dockerfile -t gb-util:latest

# run it
docker run --rm gb-util:latest --help

# push to docker hub
docker tag gb-util:latest krcourville/gb-util:latest
docker push krcourville/gb-util:latest

# Now, the image can be run AWS-deployed infrastructure
```


## References

* <https://www.gutenberg.org/ebooks/offline_catalogs.html#the-project-gutenberg-catalog-metadata-in-machine-readable-format>
* [aiohttp Client](https://us-pycon-2019-tutorial.readthedocs.io/aiohttp_client.html)
* [Python Application Layouts: A Reference](https://realpython.com/python-application-layouts)
* [Hands-on Intro to aiohttp](https://us-pycon-2019-tutorial.readthedocs.io/aiohttp_client.html)
* <https://investigate.ai/>
* <https://gmusumeci.medium.com/how-to-deploy-aws-ecs-fargate-containers-step-by-step-using-terraform-545eeac743be>

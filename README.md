# aws-batch-runner

This repo represents a Proof of Concept for using AWS Batch to run
a python-based cli on a as-needed basis.

Includes `gb-util` which simulates "ingestion" of books from the
"recent" feed on [Project Gutenberg](https://www.gutenberg.org)

## Prerequisite Installations

* Terraform
* Python: tested with 3.8
* [pyenv](https://github.com/pyenv/pyenv): highly recommended for working with
multiple versions of Python.

## Deploying the Infrastructure

```sh
pushd infrastructure
terraform init
terraform import aws_cloudwatch_log_group.aws_batch_job_log_group /aws/batch/job
popd
```

## Running the cli

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

## Docker

```sh
# build the image
docker build ./src -f ./src/Dockerfile -t gb-util:latest

# run it
docker run --rm gb-util:latest --help

```

## Deploy a new version

> TODO: make this less error-prone

1. Review current version `app_image` var in `./infrastructure/variables.tf`
2. Increment using semantic versioning: `export VERSION=x.x.x
3. build: `docker build ./src -f ./src/Dockerfile -t gb-util:latest`
4. tag: `docker tag gb-util:latest krcourville/gb-util:${VERSION}`
5. push: `docker push krcourville/gb-util:${VERSION}`
6. update Batch Job Definition:
    ```sh
    pushd infrastructure
    export TF_VAR_image_version=$VERSION
    terraform apply
    popd
    ```
7. commit changes `git add... git commit...`
8. tag the repo: `git tag $VERSION && git push --tags`


## References

* <https://www.gutenberg.org/ebooks/offline_catalogs.html#the-project-gutenberg-catalog-metadata-in-machine-readable-format>
* [aiohttp Client](https://us-pycon-2019-tutorial.readthedocs.io/aiohttp_client.html)
* [Python Application Layouts: A Reference](https://realpython.com/python-application-layouts)
* [Hands-on Intro to aiohttp](https://us-pycon-2019-tutorial.readthedocs.io/aiohttp_client.html)
* <https://investigate.ai/>
* <https://gmusumeci.medium.com/how-to-deploy-aws-ecs-fargate-containers-step-by-step-using-terraform-545eeac743be>

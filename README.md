[![Total alerts](https://img.shields.io/lgtm/alerts/g/alphagov/cyber-security-security-advisory-dashboard.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/alphagov/cyber-security-security-advisory-dashboard/alerts/) [![Language grade: JavaScript](https://img.shields.io/lgtm/grade/javascript/g/alphagov/cyber-security-security-advisory-dashboard.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/alphagov/cyber-security-security-advisory-dashboard/context:javascript) [![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/alphagov/cyber-security-security-advisory-dashboard.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/alphagov/cyber-security-security-advisory-dashboard/context:python)

# Security Advisory Dashboard

## Prerequisites

 - Check you have docker and docker-compose installed

```
docker --version
docker-compose --version
```

 - Set a GITHUB_ORG env var containing the organisation login short name
from the GitHub URL.

 - Set a TOKEN env var containing a read-only personal access token for a GitHub org
admin user. The permissions needed for the token are:

`repo`, `read:org`, `read:public_key`, `read:repo_hook`, `read:user`, `user:email`

(Alternatively the token can be retrieved from SSM if the make command
is run via aws-vault or similar to set AWS credentials.)

 - Create or change the `settings.[env].json` file


### Run an audit

```audit
make audit
```
Gets the paged repository data with vulnerability alerts

The audit process runs the api calls to collect vulnerability and
activity data from github as well as the dependabot config API to
determine which repositories have dependabot enabled.

### Run audit component tasks

You can run individual tasks from the audit process for testing.

For example to rebuild the interface route template data files you
can call the following:
```task
make task TASK=routes
```

You can call the tasks separately because the full audit takes a long
time to run.

## Run a local dev server

The `run` task currently runs the npm install and then runs the gulp tasks
to build the static assets, js and css.

```run
make run
```

## Run the tests

Run the unit tests by running

```test
make test
```

## Terraform

### Build
Before you can run the terraform you need to create a zipped lambda
deployment.

You can do that by running

```zip
make zip
```

> TODO We can probably make the terraform run the zip command

### Init
The terraform is in `build/terraform`

To init you need a `backend.tfvars`
```backend.tfvars
bucket  = "<bucket name>"
key     = "<state file path>"
region  = "eu-west-2"
encrypt = true
```

Then you can run
```init
terraform init -reconfigure -backend-config=path/to/backend.tfvars
```

### Plan or apply
You need an apply.tfvars

```apply.tfvars
region              = "eu-west-2"
bucket_prefix       = "cyber-security"
runtime             = "python3.7"

github_org          = "<github organisation shortname>"

Service             = "github-audit"
SvcOwner            = "<who to email>"
Environment         = "<should match a setting file env>"
DeployedUsing       = "Terraform"
SvcCodeURL          = "https://github.com/alphagov/cyber-security-security-advisory-dashboard"
```

Then you can run

```apply
terraform apply -var-file=path/to/apply.tfvars
```

### Find vars at
https://github.com/alphagov/cyber-security-terraform/tree/master/service/github_audit/account/103495720024

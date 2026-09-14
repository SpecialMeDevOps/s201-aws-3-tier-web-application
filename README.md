# s201-aws-3-tier-web-application
AWS 3-tier cloud-native application with React, Flask REST API, Aurora Serverless, Docker, Terraform IaC, VPC networking, Security Groups, and CloudWatch monitoring

## Local development

Run the backend tests:

```powershell
cd backend
python -m pytest -q
```

Run the full local stack with Docker:

```powershell
cd deployment
docker compose up --build
```

Open the frontend at `http://localhost:8080`. The backend health endpoint is
available at `http://localhost:5000/health`.

## Terraform validation

The development Terraform configuration is in
`infrastructure/environments/dev`. Validate it before applying:

```powershell
cd infrastructure/environments/dev
terraform init -backend=false
terraform fmt -check
terraform validate
```

The GitHub Actions workflow runs backend tests and Terraform validation on
pushes to the default branch and on pull requests.

The deployment workflows are separate: `Terraform Apply` creates or updates
the development infrastructure manually, `Terraform Destroy` removes it only
after a `DESTROY` confirmation, `Docker Build` builds without publishing, and
`Docker Push` publishes the backend image to ECR before starting a new ECS
deployment.

Configure repository secrets `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and
`TF_VAR_DB_PASSWORD` before running the AWS workflows.

## AWS deployment

Terraform creates the ECR repository and, during `terraform apply`, builds the
backend image from `backend/`, logs in to ECR, pushes the `latest` tag, and
deploys that image to ECS Fargate. Docker Desktop and the AWS CLI must be
installed and logged in before applying:

```powershell
aws sts get-caller-identity
docker version
cd infrastructure/environments/dev
$env:TF_VAR_db_password = "use-a-strong-development-password"
terraform init
terraform plan -out=tfplan
terraform apply tfplan
```

Do not commit `tfplan`, database passwords, or AWS credentials.

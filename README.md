## Overview

The goal of this repo is to build a working demo of using Google OAuth with FastAPI ans use CI/CD pipelines to deploy it on Google Cloud Run

## Getting Started

The code sits under app/main.py. Github actions are used to build and deploy the code to GCP cloud run. 

### Prerequisites

* The requirements.txt file has the list of packages needed
* You will need to create a GCP project along with credentials and OAUth screen needed. This blog does a good job of walking through the steps 
[![GCP setup] (https://blog.hanchon.live/guides/google-login-with-fastapi/)] The blog does the setup for a local deployment but by poiniting the URLs to your cloud run instance you can make it work for GCP
* Ensure that Github repository secrets are created. Check Settings > Secrets and variables > Actions section for the list of secrets
* The REDIRECT_URL will be your Cloud run URL + /auth. e.g: If your Cloud run URL is https://gplaces-tcobalueuq-uc.a.run.app/ then REDIRECT_URL is https://gplaces-tcoyalueuq-uc.a.run.app/auth. These will be the same URLS that are entered under Authorized JavaScript origins and Authorized redirect URIs during the GCP setup as in step 2 above
* The SECRET_KEY can be any string like "whatsupfastapi"
* The GCP_SA_ACCOUNT is a service account which you need to create along with service key which is stored in GCP_SA_KEY_JSON
* Give the service account the following roles : Cloud Build Service Account, Cloud Run Admin,Cloud Run Invoker,Owner,Service Account Token Creator,Service Usage Consumer,Storage Admin
* And if you are stuck at any point use Gemini to help you out 

# Forum api 
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This is REST API backend for forum like Reddit etc.

> Regular user:
* Can authenticate on the platform via login & password
  
* Can authenticate on the platform via oauth2
  
* Can register on platform
  
* Can update profile data & photo 

*  Can change\reset password 

* Can create\open topic

* Can edit\delete his own topic

* Can leave comments

* Can modify\delete comments (others should know about changes/deletion) 


or
## Installation
First, we need to clone the repository:
```
git clone https://github.com/senabo/bvblogic_test_task.git
```
You have to copy `.env.develop` as `.env` into `project/project/` 

### Quick start:
Application can be deployed with docker compose, so you need to run following commands:

```
docker-compose build
docker-compose ran web python manage.py makemigrations
docker-compose ran web python manage.py migrate
docker-compose run web python manage.py createsuperuser
docker-compose run web python manage.py test
docker-compose up
```

### or

Create postgresql database then change `.env` and comment POSTGRES_HOST (add # at the beginning of the line)

Install all required dependencies in an isolated environment:

```
cd bvblogic_test_task
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

You can launch test:

`python manage.py test`

## Oauth2 Token Authentication

You should be login via admin account to create a new app: 

http://localhost:8000/api/v1/oauth2/applications/

You'll get client id and client secret

Get your token authentication:
```
curl -X POST -d "grant_type=password&username=<user_name>&password=<password>" -u"<client_id>:<client_secret>" http://localhost:8000/api/v1/oauth2/token/ 
   ```
Oauth2 documentation is [here](https://django-oauth-toolkit.readthedocs.io/en/latest/rest-framework/getting_started.html#step-3-register-an-application)

## Swagger Documentation
Use this endpoint: http://localhost:8000/api/v1/doc/ 


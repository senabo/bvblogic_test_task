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

## Installation
First, we need to clone the repository:
```
git clone https://github.com/senabo/bvblogic_test_task.git
```
You have to copy `.env.develop` as `.env` into `project/project/` 

Create postgresql database and then change `.env`

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
## Oauth2 Token Authentication
Oauth2 endpoint: http://localhost:8000/api/v1/oauth2/
   
Oauth2 documentation is [here](https://django-oauth-toolkit.readthedocs.io/en/latest/rest-framework/getting_started.html#step-3-register-an-application)

## Swagger Documentation
Use this endpoint: http://localhost:8000/api/v1/doc/ 


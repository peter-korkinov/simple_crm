# Simple CRM

#### OpenAPI documentation available

This is Simple CRM system for companies and employees.It is set up by default for use with PostgreSQL.


It contains two apps - "companies" and "employees".

## Requirements

Django==4.1.7\
djangorestframework==3.14.0

### Additional libraries used:

drf-spectacular==0.25.1\
Faker==17.0.0\
Pillow==9.4.0\
psycopg2==2.9.5\
pytest==7.2.1\
pytest-django==4.5.2\
python-dotenv==0.21.1

## Set up
in terminal:

```bash
git clone https://github.com/peter-korkinov/simple_crm.git
```

or simply download using the url:

[https://github.com/peter-korkinov/simple_crm](https://github.com/peter-korkinov/simple_crm)

&nbsp;

Then open the main project directory in terminal and run:



```bash
pip install virtualenv # if you don't already have virtualenv installed
```
```bash
virtualenv venv # to create your new environment(called 'venv' here)
```
```bash
venv/Source/activate # to enter the virtual environment
```
```bash
pip install -r requirements.txt # to install requirements in the current environment
```
&nbsp;

The project is set up by default to use PostgreSQL configured with environment variables.
To use it in that way you need to create a ".env" file in the root directory and set the following variables in it:

```bash
DB_NAME='your db name'
DB_USER='your db username'
DB_PASS='your db password'
DB_HOST='your db host'
DB_PORT='your db port'
DEBUG=True
```

Or you can uncomment the default 'DATABASES' parameter in project's settings file and use SQLite.
(And also set the 'DEBUG' parameter to True or set ALLOWED_HOSTS)

&nbsp;


```bash 
python manage.py makemigrations # to makemigrations
```
```bash
python manage.py migrate # to migrate
```
&nbsp;


Then finally to run the project in local server use the following command:
```bash
python manage.py runserver
```

To access the **OpenAPI** documentation open:
[http://localhost:8000/api/schema/swagger-ui/](http://localhost:8000/api/schema/swagger-ui/)

&nbsp;

### To use admin panel you need to create superuser using this command

``` bash
python manage.py createsuperuser
```

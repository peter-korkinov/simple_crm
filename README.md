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
pip install -r requirements.txt
```
&nbsp;


To run the program in local server use the following command
```bash
python manage.py runserver
```

Then go to [http://localhost:8000/](http://localhost:8000/) in your browser

To access the **OpenAPI** documentation open:
[http://localhost:8000/api/schema/swagger-ui/](http://localhost:8000/api/schema/swagger-ui/)

&nbsp;


### To migrate the database

```bash 
python manage.py makemigrations
python manage.py migrate
```
&nbsp;

### To use admin panel you need to create superuser using this command

``` bash
python manage.py createsuperuser
```


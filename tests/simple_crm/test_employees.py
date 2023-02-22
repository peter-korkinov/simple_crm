import os
import pytest

from faker import Faker
from django.urls import reverse
from django.test import override_settings

from companies.models import Company
from simple_crm.settings import BASE_DIR


fake = Faker()

url = reverse('employees')


@override_settings(MEDIA_ROOT=os.path.join(BASE_DIR, 'tests', 'test_media'))
@pytest.mark.django_db
def test_create_employee_success(client, company, employee):
    this_company = Company.objects.create(**company().generate())
    this_emp_data = employee().generate()
    this_emp_data['employer'] = this_company.pk
    response = client.post(url, this_emp_data)
    data = response.data

    assert response.status_code == 201
    assert 'id' in data
    assert 'first_name' in data
    assert 'last_name' in data
    assert 'date_of_birth' in data
    assert 'photo' in data
    assert 'position' in data
    assert 'salary' in data
    assert 'employer' in data
    assert data['first_name'] == this_emp_data['first_name']
    assert data['last_name'] == this_emp_data['last_name']
    assert data['date_of_birth'] == this_emp_data['date_of_birth']
    assert data['photo'] == '/media/images/' + this_emp_data['photo'].name
    assert data['position'] == this_emp_data['position']
    assert float(data['salary']) == this_emp_data['salary']
    assert data['employer'] == this_emp_data['employer']


@override_settings(MEDIA_ROOT=os.path.join(BASE_DIR, 'tests', 'test_media'))
@pytest.mark.django_db
def test_list_all_employees_success(client, employee):
    employees = (
        client.post(url, employee().generate()),
        client.post(url, employee().generate()),
        client.post(url, employee().generate())
    )
    response = client.get(url)
    data = response.data

    assert response.status_code == 200
    assert len(data) == 3
    for i in range(len(data)):
        assert data[i]['id'] == employees[i].data['id']
        assert data[i]['first_name'] == employees[i].data['first_name']
        assert data[i]['last_name'] == employees[i].data['last_name']
        assert data[i]['date_of_birth'] == employees[i].data['date_of_birth']
        assert data[i]['photo'] == employees[i].data['photo']
        assert data[i]['position'] == employees[i].data['position']
        assert data[i]['salary'] == employees[i].data['salary']
        assert data[i]['employer'] == employees[i].data['employer']


@override_settings(MEDIA_ROOT=os.path.join(BASE_DIR, 'tests', 'test_media'))
@pytest.mark.django_db
def test_get_employee_by_id_success(client, employee):
    employees = (
        client.post(url, employee().generate()),
        client.post(url, employee().generate()),
        client.post(url, employee().generate())
    )
    this_url = url + str(employees[1].data['id']) + '/'
    response = client.get(this_url)
    data = response.data

    emp_data = employees[1].data
    assert response.status_code == 200
    assert data['id'] == emp_data['id']
    assert data['first_name'] == emp_data['first_name']
    assert data['last_name'] == emp_data['last_name']
    assert data['date_of_birth'] == emp_data['date_of_birth']
    assert data['photo'] == emp_data['photo']
    assert data['position'] == emp_data['position']
    assert data['salary'] == emp_data['salary']
    assert data['employer'] == emp_data['employer']


@override_settings(MEDIA_ROOT=os.path.join(BASE_DIR, 'tests', 'test_media'))
@pytest.mark.django_db
def test_patch_employee_success(client, employee):
    emp = client.post(url, employee().generate())
    emp_data = emp.data
    patch_data = {'date_of_birth': '1992-02-12'}
    this_url = url + str(emp_data['id']) + '/'
    response = client.patch(this_url, patch_data)
    data = response.data

    assert response.status_code == 200
    assert 'id' in data
    assert 'first_name' in data
    assert 'last_name' in data
    assert 'date_of_birth' in data
    assert 'photo' in data
    assert 'position' in data
    assert 'salary' in data
    assert 'employer' in data
    assert data['id'] == emp_data['id']
    assert data['first_name'] == emp_data['first_name']
    assert data['last_name'] == emp_data['last_name']
    assert data['date_of_birth'] == patch_data['date_of_birth']
    assert data['photo'] == emp_data['photo']
    assert data['position'] == emp_data['position']
    assert data['salary'] == emp_data['salary']
    assert data['employer'] == emp_data['employer']


@override_settings(MEDIA_ROOT=os.path.join(BASE_DIR, 'tests', 'test_media'))
@pytest.mark.django_db
def test_delete_employee_success(client, employee):
    employees = (
        client.post(url, employee().generate()),
        client.post(url, employee().generate()),
        client.post(url, employee().generate())
    )
    this_url = url + str(employees[1].data['id']) + '/'
    response = client.delete(this_url)
    remaining_response = client.get(url)

    assert response.status_code == 204
    assert len(remaining_response.data) == 2

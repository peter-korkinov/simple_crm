import os
import pytest

from faker import Faker
from django.urls import reverse
from django.test import override_settings

from companies.models import Company
from simple_crm.settings import BASE_DIR


fake = Faker()

url = reverse('companies')


@override_settings(MEDIA_ROOT=os.path.join(BASE_DIR, 'tests', 'test_media'))
@pytest.mark.django_db
def test_create_company_success(client, company):
    this_company = company().generate()
    response = client.post(url, this_company)
    data = response.data

    assert response.status_code == 201
    assert 'id' in data
    assert 'name' in data
    assert 'logo' in data
    assert 'description' in data
    assert data['id'] == 1
    assert data['name'] == this_company['name']
    assert data['description'] == this_company['description']


@override_settings(MEDIA_ROOT=os.path.join(BASE_DIR, 'tests', 'test_media'))
@pytest.mark.django_db
def test_create_company_name_must_be_unique(client, company):
    company1_data, company2_data = company().generate(), company().generate()
    company2_data['name'] = company1_data['name']
    client.post(url, company1_data)
    response = client.post(url, company2_data)
    data = response.data

    assert response.status_code == 400
    assert 'name' in data
    assert len(data) == 1
    assert str(data['name'][0]) == 'company with this name already exists.'


@override_settings(MEDIA_ROOT=os.path.join(BASE_DIR, 'tests', 'test_media'))
@pytest.mark.django_db
def test_list_all_companies_success(client, company):
    companies = (
        client.post(url, company().generate()),
        client.post(url, company().generate()),
        client.post(url, company().generate())
    )
    response = client.get(url)
    data = response.data

    assert response.status_code == 200
    assert len(data) == 3
    for i in range(len(data)):
        assert data[i]['id'] == companies[i].data['id']
        assert data[i]['name'] == companies[i].data['name']
        assert data[i]['logo'] == companies[i].data['logo']
        assert data[i]['description'] == companies[i].data['description']


@override_settings(MEDIA_ROOT=os.path.join(BASE_DIR, 'tests', 'test_media'))
@pytest.mark.django_db
def test_get_company_by_id_success2(client, company):
    Company.objects.create(**company().generate())
    test_target = Company.objects.create(**company().generate())
    Company.objects.create(**company().generate())
    this_path = url + str(test_target.pk) + '/'
    request = client.get(this_path)
    data = request.data

    assert request.status_code == 200
    assert data['id'] == test_target.pk
    assert data['name'] == test_target.name
    assert data['logo'] == '/media/' + test_target.logo.name
    assert data['description'] == test_target.description


@override_settings(MEDIA_ROOT=os.path.join(BASE_DIR, 'tests', 'test_media'))
@pytest.mark.django_db
def test_patch_company_record_success(client, company):
    primordial_data = company().generate()
    record = client.post(url, primordial_data)
    rec_data = record.data
    patch_data = {'name': 'new_name'}
    this_url = url + str(rec_data['id']) + '/'
    request = client.patch(this_url, patch_data)
    data = request.data

    assert request.status_code == 200
    assert data['id'] == rec_data['id']
    assert data['name'] == patch_data['name']
    assert data['logo'] == rec_data['logo']
    assert data['description'] == rec_data['description']


@override_settings(MEDIA_ROOT=os.path.join(BASE_DIR, 'tests', 'test_media'))
@pytest.mark.django_db
def test_patch_company_record_name_must_be_unique(client, company):
    com1, com2 = client.post(url, company().generate()),\
                 client.post(url, company().generate())
    patch_data = {'name': com1.data['name']}
    this_url = url + str(com2.data['id']) + '/'
    request = client.patch(this_url, patch_data)
    data = request.data

    assert request.status_code == 400
    assert 'name' in data
    assert len(data) == 1
    assert str(data['name'][0]) == 'company with this name already exists.'


@override_settings(MEDIA_ROOT=os.path.join(BASE_DIR, 'tests', 'test_media'))
@pytest.mark.django_db
def test_delete_company_record_success(client, company):
    Company.objects.create(**company().generate())
    test_target = Company.objects.create(**company().generate())
    Company.objects.create(**company().generate())
    this_path = url + str(test_target.pk) + '/'
    request = client.delete(this_path)
    request_remaining = client.get(url)

    assert request.status_code == 204
    assert request_remaining.status_code == 200
    assert len(request_remaining.data) == 2


@override_settings(MEDIA_ROOT=os.path.join(BASE_DIR, 'tests', 'test_media'))
@pytest.mark.django_db
def test_retrieve_expanded_company_success(client, company, employee):
    employees = (
        employee().generate(),
        employee().generate(),
        employee().generate()
    )
    companies = (
        client.post(url, company().generate()),
        client.post(url, company().generate())
    )
    for emp in employees:
        emp['employer'] = companies[0].data['id']
        client.post(reverse('employees'), emp)

    comp_w_emps_url = url + str(companies[0].data['id']) + '/expanded/'
    comp_w_emps = client.get(comp_w_emps_url)
    comp_wo_emps_url = url + str(companies[1].data['id']) + '/expanded/'
    comp_wo_emps = client.get(comp_wo_emps_url)

    assert comp_w_emps.status_code == 200
    assert comp_wo_emps.status_code == 200
    assert len(comp_w_emps.data['employees']) == 3
    assert len(comp_wo_emps.data['employees']) == 0

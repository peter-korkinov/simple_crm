import os
import shutil
import pytest

from io import BytesIO
from PIL import Image
from faker import Faker
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile

from simple_crm.settings import BASE_DIR


fake = Faker()


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def company():
    class Dummy:
        def __init__(self):
            self.some_logo = self.generate_logo()

        @staticmethod
        def generate_logo():
            a_logo = SimpleUploadedFile(
                name=fake.file_name(extension='svg'),
                content=fake.binary(length=64),
                content_type='image/svg+xml'
            )
            return a_logo

        def generate(self):
            return {
                'name': fake.company(),
                'logo': self.some_logo,
                'description': fake.text()
            }

    yield Dummy
    path = os.path.join(BASE_DIR, 'tests', 'test_media', 'logos')
    shutil.rmtree(path)


@pytest.fixture
def employee():
    class Dummy:
        def __init__(self):
            self.some_image = self.generate_image()

        @staticmethod
        def generate_image():
            f = BytesIO()
            image = Image.new("RGB", (100, 100))
            image.save(f, 'png')
            f.seek(0)
            an_image = SimpleUploadedFile(
                name=fake.file_name(extension='jpeg'),
                content=f.read(),
                content_type='image/jpeg'
            )
            return an_image

        def generate(self):
            return {
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
                'date_of_birth': fake.date(),
                'photo': self.some_image,
                'position': fake.job(),
                'salary': fake.pyfloat(left_digits=6, right_digits=2,
                                       positive=True, max_value=999999.99)

            }

    yield Dummy
    path = os.path.join(BASE_DIR, 'tests', 'test_media', 'images')
    shutil.rmtree(path)


# @pytest.fixture
# def company(some_logo):
#     class Dummy:
#         def generate(self):
#             return {
#                 'name': fake.name(),
#                 'logo': some_logo,
#                 'description': fake.text()
#             }
#     return Dummy
#
#
# @pytest.fixture
# def some_logo():
#     some_logo = SimpleUploadedFile(
#         name=fake.file_name(extension='svg'),
#         content=b'file_content',
#         content_type='image/svg+xml'
#     )
#     yield some_logo
#     path = os.path.join(BASE_DIR, 'logos', some_logo.name)
#     os.remove(path)


# @pytest.fixture
# def company():
#     class Dummy:
#         def __init__(self):
#             self.logo = self.some_logo()
#
#         @staticmethod
#         def some_logo():
#             a_logo = SimpleUploadedFile(
#                 name=fake.file_name(extension='svg'),
#                 content=b'file_content',
#                 content_type='image/svg+xml'
#             )
#             yield a_logo
#             path = os.path.join(BASE_DIR, 'logos', a_logo.name)
#             os.remove(path)
#
#         def generate(self):
#             return {
#                 'name': fake.name(),
#                 'logo': self.logo,
#                 'description': fake.text()
#             }
#     return Dummy


# def some_logo():
#     a_logo = SimpleUploadedFile(
#         name=fake.file_name(extension='svg'),
#         content=b'file_content',
#         content_type='image/svg+xml'
#     )
#     yield a_logo
#     path = os.path.join(BASE_DIR, 'logos', a_logo.name)
#     os.remove(path)


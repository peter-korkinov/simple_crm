from rest_framework import serializers

from employees.serializers import EmployeeSerializer
from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class ExpandedCompanySerializer(serializers.ModelSerializer):
    employees = EmployeeSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Company
        fields = ['name', 'logo', 'description', 'employees']

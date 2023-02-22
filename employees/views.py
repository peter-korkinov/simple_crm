from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Employee
from .serializers import EmployeeSerializer


@extend_schema(
        request=EmployeeSerializer,
        responses=EmployeeSerializer
)
class ListCreateEmployeesView(APIView):
    """
    A view for creating employees and listing them.
    """

    @extend_schema(
        summary='List all employees'
    )
    def get(self, request):
        """
        Lists all records of employees.
        """
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary='Add new employee'
    )
    def post(self, request):
        """
        Creates an employee record.
        """
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
        request=EmployeeSerializer,
        responses=EmployeeSerializer
)
class RetrieveUpdateDeleteEmployeeView(APIView):
    """
    A view that takes int:pk as an argument and provides get, patch and delete
    functionality for the employee records.
    """

    @extend_schema(
        summary='Find employee by ID'
    )
    def get(self, request, pk):
        """
        Returns the employee record with the provided pk.
        """
        employee = get_object_or_404(Employee, pk=pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    @extend_schema(
        summary='Update employee'
    )
    def patch(self, request, pk):
        """
        Partially updates the employee record with the provided pk and
        returns the updated employee record.
        """
        employee = get_object_or_404(Employee, pk=pk)
        serializer = EmployeeSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary='Delete employee'
    )
    def delete(self, request, pk):
        """
        Deletes the employee record with the provided pk and
        returns empty body response.
        """
        employee = get_object_or_404(Employee, pk=pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

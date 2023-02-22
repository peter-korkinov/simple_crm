from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Company
from .serializers import CompanySerializer, ExpandedCompanySerializer


@extend_schema(
        request=CompanySerializer,
        responses=CompanySerializer
)
class ListCreateCompaniesView(APIView):
    """
    A view for creating companies and listing them.
    """

    @extend_schema(
        summary='List companies'
    )
    def get(self, request):
        """
        Lists all records of companies.
        """
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary='Add new company'
    )
    def post(self, request):
        """
        Creates a company record.
        """
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
        request=CompanySerializer,
        responses=CompanySerializer
)
class RetrieveUpdateDeleteCompanyView(APIView):
    """
    A view that takes int:pk as an argument and provides get, patch and delete
    functionality for the company records.
    """

    @extend_schema(
        summary='Find company by ID'
    )
    def get(self, request, pk):
        """
        Returns the company record with the provided pk.
        """
        company = get_object_or_404(Company, pk=pk)
        serializer = CompanySerializer(company)
        return Response(serializer.data)

    @extend_schema(
        summary='Update company'
    )
    def patch(self, request, pk):
        """
        Partially updates the company record with the provided pk and
        returns the updated record.
        """
        company = get_object_or_404(Company, pk=pk)
        serializer = CompanySerializer(company, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary='Delete company'
    )
    def delete(self, request, pk):
        """
        Deletes the company record with the provided pk and
        returns empty body response.
        """
        company = get_object_or_404(Company, pk=pk)
        company.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
        request=ExpandedCompanySerializer,
        responses=ExpandedCompanySerializer,
)
class RetrieveExpandedCompanyView(APIView):
    """
    A view for retrieving a concrete company and all of its employees.
    """

    @extend_schema(
        summary='Find company by ID with expanded employees field'
    )
    def get(self, request, pk):
        """
        Returns the company record with the provided pk with additional field
        with all the employee records that are related to that company.
        """
        company = get_object_or_404(Company, pk=pk)
        serializer = ExpandedCompanySerializer(company)
        return Response(serializer.data)

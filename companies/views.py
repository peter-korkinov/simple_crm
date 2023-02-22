from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Company
from .serializers import CompanySerializer, ExpandedCompanySerializer


class ListCreateCompaniesView(APIView):
    """
    A view for creating companies and listing them.
    """

    def get(self, request):
        """
        Lists all records of companies.
        """
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Creates a company record.
        """
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RetrieveUpdateDeleteCompanyView(APIView):
    """
    A view that takes int:pk as an argument and provides get, patch and delete
    functionality for the company records.
    """

    def get(self, request, pk):
        """
        Returns the company record with the provided pk.
        """
        company = get_object_or_404(Company, pk=pk)
        serializer = CompanySerializer(company)
        return Response(serializer.data)

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

    def delete(self, request, pk):
        """
        Deletes the company record with the provided pk and
        returns empty body response.
        """
        company = get_object_or_404(Company, pk=pk)
        company.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RetrieveExpandedCompanyView(APIView):
    """
    A view for retrieving a concrete company and all of its employees.
    """

    def get(self, request, pk):
        """
        Returns the company record with the provided pk with additional field
        with all the employee records that are related to that company.
        """
        company = get_object_or_404(Company, pk=pk)
        serializer = ExpandedCompanySerializer(company)
        return Response(serializer.data)

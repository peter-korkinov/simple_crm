from django.urls import path

from .views import ListCreateCompaniesView, RetrieveUpdateDeleteCompanyView,\
    RetrieveExpandedCompanyView


urlpatterns = [
    path('', ListCreateCompaniesView.as_view(), name='companies'),
    path('<int:pk>/expanded/', RetrieveExpandedCompanyView.as_view(), name='company_expanded'),
    path('<int:pk>/', RetrieveUpdateDeleteCompanyView.as_view(), name='company')
]

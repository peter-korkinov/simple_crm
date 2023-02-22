from django.urls import path

from .views import ListCreateEmployeesView, RetrieveUpdateDeleteEmployeeView


urlpatterns = [
    path('', ListCreateEmployeesView.as_view(), name='employees'),
    path('<int:pk>/', RetrieveUpdateDeleteEmployeeView.as_view(), name='employee')
]

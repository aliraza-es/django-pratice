from django.urls import path
from .views import CompanyListCreateView, CompanyRetrieveUpdateDeleteView

urlpatterns = [
    path('companies/', CompanyListCreateView.as_view(), name='company-list-create'),
    path('companies/<int:pk>/', CompanyRetrieveUpdateDeleteView.as_view(), name='company-detail'),
]

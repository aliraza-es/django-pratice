from rest_framework import generics
from .models import Company
from .serializers import CompanySerializer
from rest_framework.permissions import IsAuthenticated

class CompanyListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class CompanyRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Company.objects.all()
    serializer_class = CompanySerializer

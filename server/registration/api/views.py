from rest_framework import viewsets
from registration.api.serializers import *
from registration.models import *

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class TrainingViewSet(viewsets.ModelViewSet):
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer

class EmployeeRegistrationViewSet(viewsets.ModelViewSet):
    queryset = EmployeeRegistration.objects.all()
    serializer_class = EmployeeRegistrationSerializer
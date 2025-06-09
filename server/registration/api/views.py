from rest_framework import viewsets
from registration.api.serializers import EmployeeSerializer, TrainingSerializer
from registration.models import Employee, Training

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class TrainingViewSet(viewsets.ModelViewSet):
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer
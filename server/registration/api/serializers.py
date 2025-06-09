from rest_framework import serializers
from registration.models import Employee, Training

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'slug', 'photo', 'name', 'cpf']

class TrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training
        fields = ['id', 'model']

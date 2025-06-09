from django.urls import path
from .views import create_employee, create_faces_collection, face_detection

urlpatterns = [
    path('', create_employee, name='create_employee'),
    path('create_faces_collection/<int:employee_id>', create_faces_collection, name='create_faces_collection'),
    path('face_detection/', face_detection, name='face_detection')
]
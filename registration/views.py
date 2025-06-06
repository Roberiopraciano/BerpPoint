from django.shortcuts import render, redirect
from .forms import EmployeeForm, FaceCollectionForm
from .models import Employee, FaceCollection

def create_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)

        if form.is_valid():
            employee = form.save()
            return redirect('create_faces_collection', employee_id=employee.id)
    else:
        form = EmployeeForm()
    return render(request, 'create_employee.html', {'form': form})


def create_faces_collection(request, employee_id):
    employee = Employee.objects.get(id=employee_id)

    if request.method == 'POST':
        form = FaceCollectionForm(request.POST, request.FILES)

        if form.is_valid():
            for image in request.FILES.getlist('images'):
                FaceCollection.objects.create(employee=employee, image=image)
    else:
        form = FaceCollectionForm()
        
    context = {
        'employee': employee,
        'form': form
    }
    
    return render(request, 'create_faces_collection.html', context)
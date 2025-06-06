from django.shortcuts import render, redirect
from .forms import EmployeeForm
from .models import Employee
from django.http import StreamingHttpResponse
from .camera import VideoCamera

camera_detection = VideoCamera()

def gen_detect_face(camera_detection):
    while True:
        frame = camera_detection.get_camera()

        if frame is None:
            continue

        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def face_detection(request):
    return StreamingHttpResponse(gen_detect_face(camera_detection), content_type='multipart/x-mixed-replace; boundary=frame')


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
    print(employee_id)
    employee = Employee.objects.get(id=employee_id)

    context = {
        'employee': employee,
        'face_detection': face_detection,
    }

    return render(request, 'create_faces_collection.html', context)
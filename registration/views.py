import cv2
import os
from django.shortcuts import render, redirect
from .forms import EmployeeForm
from .models import Employee, FaceCollection
from django.http import StreamingHttpResponse
from .camera import VideoCamera

camera_detection = VideoCamera()

def gen_detect_face(camera_detection):
    while True:
        frame = camera_detection.detect_face()

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

    btn_clicked = request.GET.get('clicked', 'False') == 'True'

    context = {
        'employee': employee,
        'face_detection': face_detection,
        'btn_value': btn_clicked
    }

    if btn_clicked:
        print("Cliquei em Extrair Imagens!")
        context = face_extract(context, employee)

    return render(request, 'create_faces_collection.html', context)


def extract(camera_detection, employee):
    sample = 0
    numSamples = 10
    width, height = 220, 220
    file_paths = []

    while sample < numSamples:
        ret, frame = camera_detection.get_camera()
        crop = camera_detection.sample_faces(frame)

        if crop is not None:
            sample += 1

            face = cv2.resize(crop, (width, height))
            gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
    
            file_name_path = f'./tmp/{employee.slug}_{sample}.jpg'
            cv2.imwrite(file_name_path, gray)
            file_paths.append(file_name_path)

        else:
            print("Face não encontrada")
        
        if sample >= numSamples:
            break

    camera_detection.restart()
    return file_paths


def face_extract(context, employee):
    num_collections = FaceCollection.objects.filter(employee__slug=employee.slug).count()

    if num_collections >= 10:
        context['erro'] = 'Limite máximo de coletas atingido.'
    else:
        files_paths = extract(camera_detection, employee)

        for path in files_paths:
            collect_face = FaceCollection.objects.create(employee=employee)
            collect_face.image.save(os.path.basename(path), open(path, 'rb'))
            os.remove(path)

        context['file_paths'] = FaceCollection.objects.filter(employee__slug=employee.slug)
        context['extract_ok'] = True

    return context
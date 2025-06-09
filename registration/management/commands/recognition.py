import cv2
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from registration.models import Employee, Training

class Command(BaseCommand):
    help = "Comando para teste de reconhecimento facial com exibição ao vivo da câmera"

    def handle(self, *args, **kwargs):
        self.recognize_faces()

    def recognize_faces(self):
        face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        recognizer = cv2.face.EigenFaceRecognizer_create()

        training = Training.objects.first()

        if not training:
            print("Modelo de treinamento não encontrado.")
            return

        model_path = os.path.join(settings.MEDIA_ROOT, training.model.name)
        recognizer.read(model_path)

        camera = cv2.VideoCapture(0)
        width, height = 220, 220
        font = cv2.FONT_HERSHEY_COMPLEX_SMALL

        while True:
            ret, frame = camera.read()

            if not ret:
                print("Erro ao acessar a câmera.")
                break

            frame = cv2.resize(frame, (480, 360))
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            detected_faces = face_cascade.detectMultiScale(gray, minNeighbors=20, minSize=(30, 30), maxSize=(400, 400))
                                                             
            for (x,y,l,a) in detected_faces:
                imagemFace = cv2.resize(gray[y:y+a,x:x+l], (width, height))
                cv2.rectangle(frame, (x,y), (x+l,y+a), (0,255,0), 2)
                label, result = recognizer.predict(imagemFace)
                print(label)
                employee = Employee.objects.get(id=label)

                if employee:
                    cv2.putText(frame, str(employee.name).strip("(), '"), (x, y + a + 30), font, 1, (0, 255, 0), 2)
                else:
                    cv2.putText(frame, "Nenhum user encontrado", (x, y + a + 30), font, 1, (0, 0, 255), 2)
                                                         
            cv2.imshow("Reconhecimento Facial", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        camera.release()
        cv2.destroyAllWindows()
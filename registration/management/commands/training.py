import os
import numpy as np
import cv2
from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from registration.models import FaceCollection, Training

class Command(BaseCommand):
    help = "Treina o classificador Eigen para reconhecimento facial"

    def handle(self, *args, **kwargs):
        self.training_face()

    def training_face(self):
        self.stdout.write(self.style.WARNING("Iniciando treinamento com base de informações"))
        print(cv2.__version__)

        eigenFace = cv2.face.EigenFaceRecognizer_create(num_components=50, threshold=0)

        faces, labels = [], []
        error_count = 0

        for sample in FaceCollection.objects.all():
            image_file = sample.image.url.replace('/media/roi/', '')
            image_path = os.path.join(settings.MEDIA_ROOT, 'roi', image_file)

            if not os.path.exists(image_path):
                print(f"Caminho não encontrado: {image_path}")
                error_count += 1
                continue

            image = cv2.imread(image_path)

            if image is None:
                print(f"Erro ao carregar a imagem: {image_path}")
                error_count += 1
                continue
            
            faceImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faceImage = cv2.resize(faceImage, (220, 220))
            faces.append(faceImage)
            labels.append(sample.employee.id)

        if not faces:
            print("Nenhuma face encontrada para treinamento.")
            return

        try:
            eigenFace.train(np.array(faces), np.array(labels))
            print(f"{len(faces)} imagens treinadas com sucesso.")

            model_filename = os.path.join(settings.BASE_DIR, 'eigenClassificator.yml')
            eigenFace.write(model_filename)

            with open(model_filename, 'rb') as f:
                training, created = Training.objects.get_or_create()
                training.model.save('eigenClassificator.yml', File(f))

            os.remove(model_filename)

            if error_count > 0:
                self.stdout.write(self.style.ERROR(f"{error_count} imagem(ns) com erro no carregamento"))

            self.stdout.write(self.style.SUCCESS("TREINAMENTO EFETUADO"))
        except Exception as e:
            print(f"Erro durante o treinamento: {e}")
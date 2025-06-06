import cv2

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

        if not self.video.isOpened():
            print("Erro ao acessar a câmera.")

    def __del__(self):
        self.video.release()

    def restart(self):
        self.video.release()
        self.video = cv2.VideoCapture(0)

    def get_camera(self):
        ret, frame = self.video.read()

        if not ret:
            print("Falha ao capturar o frame.")
            return None

        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
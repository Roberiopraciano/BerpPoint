import cv2 
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivy.graphics.texture import Texture

Window.size = (360, 600)

class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = MDBoxLayout(orientation="vertical")
        self.add_widget(layout) 
        self.image = Image()
        layout.add_widget(self.image)


    def load_video(self, *args):
        ret, frame = self.cap.read()

        if not ret:
            print("Falha ao capturar o frame")
            return
        
        height, width, _ = frame.shape

        center_x, center_y = int(width / 2), int(height / 2)
        a, b = 140, 180
        color = (144, 238, 144)

        cv2.ellipse(frame, (center_x, center_y), (a, b), 0, 0, 360, color, 10)

        buffer = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt="bgr")
        texture.blit_buffer(buffer, colorfmt="bgr", bufferfmt="ubyte")
        self.image.texture = texture


    def open_camera_for_recognition(self):
        for widget in self.children:
            if isinstance(widget, MDLabel):
                self.remove_widget(widget)

        self.cap = cv2.VideoCapture(0)

        if self.cap.isOpened():
            print("Mostrando a câmera")
            Clock.schedule_interval(self.load_video, 1.0 / 60.0)
        else:
            print("Falha ao abrir a câmera")


class ScreenManagerApp(ScreenManager):
    def open_camera_for_recognition(self):
        self.get_screen('main').open_camera_for_recognition()

class MainApp(MDApp):
    def build(self):
        return Builder.load_string("""
ScreenManagerApp:
    MainScreen:
        name: "main"
        MDLabel:
            text: "Clique no botão para reconhecimento"
            halign: "center"
            theme_text_color: "Secondary"

        MDRaisedButton:
            text: "Iniciar Reconhecimento"
            size_hint: None, None
            size: "200dp", "50dp"
            pos_hint: {"center_x": 0.5, "center_y": 0.1}
            on_press: root.open_camera_for_recognition()
""")

if __name__ == '__main__':
    MainApp().run()
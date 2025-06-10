import cv2
from datetime import datetime

from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.graphics.texture import Texture

from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager

from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout

Window.size = (360, 600)

class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Remover o layout programático - usar apenas o KV

    def load_video(self, *args):
        ret, frame = self.cap.read()

        if not ret:
            print("Falha ao capturar o frame")
            return
        
        print("Frame capturado com sucesso")
        
        height, width, _ = frame.shape
        center_x, center_y = int(width / 2), int(height / 2)
        a, b = 140, 180
        x1, y1 = center_x - a, center_y - b
        x2, y2 = center_x + a, center_y + b

        cv2.ellipse(frame, (center_x, center_y), (a, b), 0, 0, 360, (144, 238, 144), 6)

        buffer = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt="bgr")
        texture.blit_buffer(buffer, colorfmt="bgr", bufferfmt="ubyte")
        
        # Verificar se o widget existe antes de atribuir a textura
        try:
            if hasattr(self.ids, 'camera_image'):
                self.ids.camera_image.texture = texture
                print("Textura aplicada ao camera_image")
            else:
                print("Widget camera_image não encontrado!")
        except Exception as e:
            print(f"Erro ao aplicar textura: {e}")

    def open_camera_for_recognition(self):
        if hasattr(self, "cap") and self.cap.isOpened():
            return
        
        print("Iniciando câmera...")
        
        # Esconder a imagem estática e mostrar a câmera
        try:
            self.ids.headimage.opacity = 0
            self.ids.camera_image.opacity = 1
            print("Opacidade alterada - headimage: 0, camera_image: 1")
        except Exception as e:
            print(f"Erro ao alterar opacidade: {e}")

        for widget in self.children:
            if isinstance(widget, MDLabel):
                self.remove_widget(widget)

        self.cap = cv2.VideoCapture(0)

        if self.cap.isOpened():
            print("Câmera aberta com sucesso")
            Clock.schedule_interval(self.load_video, 1.0 / 60.0)
        else:
            print("Falha ao abrir a câmera")

    def stop_camera(self):
        """Para a câmera e volta para a imagem inicial"""
        if hasattr(self, "cap") and self.cap.isOpened():
            Clock.unschedule(self.load_video)
            self.cap.release()
            print("Câmera fechada")
        
        # Voltar para a imagem inicial
        self.ids.headimage.opacity = 1
        self.ids.camera_image.opacity = 0
        
    def show_recognized_user(self):
        self.manager.current = 'user'
        
        employee = {
            "photo": "./assets/test.jpg",
            "name": "Francisco Hermeson",
            "cpf": "123.456.789-10",
        }

        user_screen = self.manager.get_screen('user')
        user_screen.ids.photo.source = employee["photo"]
        user_screen.ids.name.text = f"Nome: {employee['name']}"
        user_screen.ids.cpf.text = f"CPF: {employee['cpf']}"
        user_screen.ids.datetime.text = f"Data e Hora: {datetime.now().strftime('%d/%m/%Y às %H:%M')}"

        user_screen.ids.card.opacity = 1


class UserScreen(MDScreen):
    pass


class ReceiptScreen(MDScreen):
    pass


class ScreenManagerApp(ScreenManager):
    def open_camera_for_recognition(self):
        self.get_screen('main').open_camera_for_recognition()


class MainApp(MDApp):
    def build(self):
        return Builder.load_string("""
ScreenManagerApp:
    MainScreen:
    UserScreen:
    ReceiptScreen:
                                                        
<MainScreen>:
    name: "main"
                                   
    MDScreen:
        md_bg_color: 0.941, 0.957, 0.973, 1

        MDTopAppBar:
            title: "Reconhecimento"
            specific_text_color: 1, 1, 1, 1
            anchor_title: "center"
            md_bg_color: 0.173, 0.243, 0.314, 1
            elevation: 0.5
            pos_hint: {"top": 1}
                                   
        # Imagem inicial (estática)
        MDCard:
            id: headimage
            size_hint: None, None
            size: "300dp", "300dp"
            pos_hint: {"center_x": 0.5, "center_y": 0.6}

            AsyncImage:
                size_hint: (1, 1)
                pos_hint: {'center_x': 0.5}
                source: './assets/test.jpg'
        
        # Widget da câmera (inicialmente invisível)
        Image:
            id: camera_image
            size_hint: None, None
            size: "300dp", "300dp"
            pos_hint: {"center_x": 0.5, "center_y": 0.6}
            opacity: 0
                                   
        MDRaisedButton:
            text: 'Registrar'
            font_size: '20sp'
            pos_hint: {'center_x': 0.5, 'center_y': 0.25}
            md_bg_color: 1, 0.388, 0.278, 1
            size_hint: (0.7, 0.1)
            elevation: 0.5
            on_press: root.open_camera_for_recognition()
                                   
<UserScreen>:
    name: "user"
                                   
    MDScreen:
        md_bg_color: 0.941, 0.957, 0.973, 1
                                   
        MDTopAppBar:
            title: "Usuário Identificado"
            specific_text_color: 1, 1, 1, 1
            anchor_title: "center"
            md_bg_color: 0.173, 0.243, 0.314, 1
            elevation: 0.5
            pos_hint: {"top": 1}
        
        MDCard:
            id: card
            size_hint: None, None
            size: "280dp", "300dp"
            pos_hint: {"center_x": 0.5, "center_y": 0.6}
            opacity: 0
                                   
            BoxLayout:
                orientation: "vertical"
                padding: "10dp"
                spacing: "10dp"
                                   
                AsyncImage:
                    id: photo
                    size_hint: (1, 0.5)
                    pos_hint: {"center_x": 0.5}
                                   
                MDLabel:
                    id: name
                    adaptive_size: True
                    theme_text_color: "Secondary"
                    size_hint_y: None
                    pos_hint: {"center_x": .5, "center_y": .5}
                    padding: "4dp", "4dp"
                                    
                MDLabel:
                    id: cpf
                    adaptive_size: True
                    theme_text_color: "Secondary"
                    size_hint_y: None
                    pos_hint: {"center_x": .5, "center_y": .5}
                    padding: "4dp", "4dp"
                                    
                MDLabel:
                    id: datetime
                    adaptive_size: True
                    theme_text_color: "Secondary"
                    size_hint_y: None
                    pos_hint: {"center_x": .5, "center_y": .5}
                    padding: "4dp", "4dp"
                                   
        MDRaisedButton:
            text: 'Confirmar'
            font_size: '20sp'
            pos_hint: {'center_x': 0.5, 'center_y': 0.25}
            size_hint: (0.7, 0.1)
            elevation: 0.5
            md_bg_color: 0.298, 0.686, 0.314, 1
            on_press: root.manager.current = 'receipt'
                                   
        MDRaisedButton:
            text: 'Não sou eu'
            font_size: '20sp'
            pos_hint: {'center_x': 0.5, 'center_y': 0.1}
            size_hint: (0.7, 0.1)
            elevation: 0.5
            md_bg_color: 0.9, 0.3, 0.3, 1
            on_press: root.manager.current = 'main'

                                   
<ReceiptScreen>:
    name: "receipt"
    MDScreen:
        md_bg_color: 0.941, 0.957, 0.973, 1
                                   
        MDTopAppBar:
            title: "Comprovante"
            specific_text_color: 1, 1, 1, 1
            anchor_title: "center"
            md_bg_color: 0.173, 0.243, 0.314, 1
            elevation: 0.5
            pos_hint: {"top": 1}
                                   
        MDCard:
            id: receipt_card
            size_hint: None, None
            size: "280dp", "300dp"
            md_bg_color: 1.0, 0.976, 0.912, 1
            pos_hint: {"center_x": 0.5, "center_y": 0.6}
            opacity: 1
                                   
            BoxLayout:
                orientation: "vertical"
                padding: "10dp"
                spacing: "10dp"
                                   
                MDLabel:
                    text: 'Comprovante'
                    halign: 'center'

        MDRaisedButton:
            text: 'Fechar'
            font_size: '20sp'
            pos_hint: {'center_x':0.5, 'center_y':0.2}
            md_bg_color: 1, 0.388, 0.278, 1
            size_hint: (0.7, 0.1)
            elevation: 0.5
            on_press: root.manager.current = 'main'
""")

if __name__ == '__main__':
    MainApp().run()
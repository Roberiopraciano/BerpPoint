from kivy.app import App
from kivy.uix.image import Image

class MyApp(App):
    def build(self):
        img = Image(source='../assets/test.jpg')
        return img

if __name__ == '__main__':
    MyApp().run()
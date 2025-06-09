from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Button(text='Botão 1'))
        layout.add_widget(Button(text='Botão 2'))
        
        return layout

if __name__ == '__main__':
    MyApp().run()
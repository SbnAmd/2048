from kivy.app import App
from kivy.uix.label import Label


class app_2048(App):
    def build(self):
        return Label(text="Hello World")
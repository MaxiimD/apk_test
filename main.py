from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import requests


class Interface(FloatLayout):
    def display_information(self):
        data = self.ids.textInput.text
        self.ids.label.text = data
        res = requests.get(
            'https://communityconnect1234-default-rtdb.europe-west1.firebasedatabase.app/Billboard.json')


class ProjectApp(App):
    def build(self):
        return Interface()


ProjectApp().run()


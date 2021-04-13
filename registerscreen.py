from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

Builder.load_file('registerscreen.kv')

class RegisterScreen(Screen):
    pass

class MainApp(MDApp):
    def build(self):
        return RegisterScreen()

#MainApp().run()
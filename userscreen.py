from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

Builder.load_file('userscreen.kv')

class User_Screen(Screen):
    pass

class MainApp(MDApp):
    def build(self):
        return User_Screen()

#MainApp().run()
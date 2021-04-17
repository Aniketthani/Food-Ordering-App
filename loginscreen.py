from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder



Builder.load_file('loginscreen.kv')

class LoginScreen(Screen):
    pass

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette="Red"
        self.theme_cls.theme_style="Light"

        return LoginScreen() 

#MainApp().run()

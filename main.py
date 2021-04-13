from kivy.core.window import Window
Window.size=(360,550)
from kivymd.app import MDApp
from loginscreen import LoginScreen
from registerscreen import RegisterScreen
from kivy.uix.screenmanager import ScreenManager

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette="Red"
        self.theme_cls.theme_style="Light"

        self.sm=ScreenManager()
        self.lgscreen=LoginScreen(name='login')
        self.sm.add_widget(self.lgscreen)
        self.regscreen=RegisterScreen(name='register')
        self.sm.add_widget(self.regscreen)
        self.sm.current="login"

        return self.sm

MainApp().run()
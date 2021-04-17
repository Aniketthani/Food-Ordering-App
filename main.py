from kivy.core.window import Window
#Window.size=(360,550)
Window.softinput_mode = 'below_target' #or pan
from kivymd.app import MDApp
from loginscreen import LoginScreen
from register_for_users_screen import Register_User_Screen
from kivy.uix.screenmanager import ScreenManager
from register_for_restaurants_screen import Register_Restaurant_Screen


class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette="Red"
        self.theme_cls.theme_style="Light"

        self.sm=ScreenManager()
        self.lgscreen=LoginScreen(name='login')
        self.sm.add_widget(self.lgscreen)
        self.reg_user_screen=Register_User_Screen(name='register_user')
        self.sm.add_widget(self.reg_user_screen)
        self.reg_restaurant_screen=Register_Restaurant_Screen(name='register_restaurant')
        self.sm.add_widget(self.reg_restaurant_screen)
        self.sm.current="login"

        return self.sm

MainApp().run()
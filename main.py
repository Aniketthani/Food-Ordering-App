from kivy.core.window import Window
#Window.size=(360,550)
Window.softinput_mode = 'below_target' #or pan
from kivymd.app import MDApp
from loginscreen import LoginScreen
from register_for_users_screen import Register_User_Screen
from kivy.uix.screenmanager import ScreenManager
from register_for_restaurants_screen import Register_Restaurant_Screen
from userscreen import User_Screen
from restaurantscreen import Restaurant_Screen
try:
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
except:
    pass


class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette="Red"
        self.theme_cls.theme_style="Light"

        self.sm=ScreenManager()
        self.sm.lgscreen=LoginScreen(name='login')
        self.sm.add_widget(self.sm.lgscreen)
        self.sm.reg_user_screen=Register_User_Screen(name='register_user')
        self.sm.add_widget(self.sm.reg_user_screen)
        self.sm.reg_restaurant_screen=Register_Restaurant_Screen(name='register_restaurant')
        self.sm.add_widget(self.sm.reg_restaurant_screen)

        self.sm.userscreen=User_Screen(name='userscreen')
        self.sm.add_widget(self.sm.userscreen)

        self.sm.restaurantscreen=Restaurant_Screen(name='restaurantscreen')
        self.sm.add_widget(self.sm.restaurantscreen)

        self.sm.current="login"

        return self.sm

MainApp().run()
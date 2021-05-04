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
from kivymd.uix.picker import MDDatePicker
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
        
        self.sm.datepicker=MDDatePicker()
        with open("session.txt","r") as f:
            matter=f.read()
            if not matter:
                self.sm.current="login"
            else:
                if matter.split("-")[2]=="r":
                    self.sm.current="restaurantscreen"
                    self.sm.restaurantscreen.r_name=matter.split("-")[1]
                    self.sm.restaurantscreen.Id=str(matter.split("-")[0])
                    self.sm.restaurantscreen.load_order_list()
                    self.sm.datepicker.bind(on_save=self.sm.restaurantscreen.save_date,on_cancel=self.sm.restaurantscreen.cancel_date)
                elif matter.split("-")[2]=="u":
                    self.sm.current="userscreen"
                    self.sm.userscreen.userid=str(matter.split("-")[0])
                    self.sm.userscreen.username=matter.split("-")[1]
            

        

        return self.sm

MainApp().run()
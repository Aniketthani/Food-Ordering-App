from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import ObjectProperty,StringProperty
from kivy.uix.boxlayout import BoxLayout

Builder.load_file('restaurantscreen.kv')

class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

class Restaurant_Screen(Screen):
    r_name=StringProperty()
    Id=StringProperty()
    veg=None
    def veg_radio_selection(self,is_veg,*args):
        if is_veg:
            if self.ids.veg.active:
                self.veg=True
                
            else:
                self.veg=None
                
        else:
            if self.ids.nonveg.active:
                self.veg=False
                
            else:
                self.veg=None
        
    
        


class MainApp(MDApp):
    def build(self):
        return Restaurant_Screen()

MainApp().run()
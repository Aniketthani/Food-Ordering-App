from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from config import connect_to_database
from kivymd.uix.card import MDCard
from kivy.graphics import Color,RoundedRectangle
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivymd.uix.label import MDLabel
from io import BytesIO
from functools import partial
from kivymd.uix.list import OneLineAvatarIconListItem,IconRightWidget

cursor,mydb=connect_to_database()

Builder.load_file('userscreen.kv')

class MyCard(MDCard):
    def __init__(self,**kwargs):
        super(MyCard,self).__init__(**kwargs)

class FoodCard(MDCard):
    def __init__(self,**kwargs):
        super(FoodCard,self).__init__(**kwargs)

        

class User_Screen(Screen):
    def __init__(self,**kwargs):
        super(User_Screen,self).__init__(**kwargs)
        Window.bind(on_keyboard=self.events)
        self.display_restaurants()

    def navigate_back(self,cur_screen,*args):
        if cur_screen=="food_menu":
            self.ids.orders_sm.current="restaurant"
        elif cur_screen=="submenu":
            self.ids.orders_sm.current="food_menu"
    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''

        if keyboard in (1001, 27):
            if self.ids.orders_sm.current=="submenu":

                self.ids.orders_sm.current="food_menu"
            elif self.ids.orders_sm.current=="food_menu":
                self.ids.orders_sm.current="restaurant"
        return True
    def display_food_menu(self,res_id,*args):
        self.ids.food_menu.clear_widgets()
        self.ids.orders_sm.current="food_menu"

        sql=f"Select Distinct Category from food_items Where Restaurant_Id='{res_id}'"
        cursor.execute(sql)
        res=cursor.fetchall()

        for c in res:
            item=OneLineAvatarIconListItem(text=c[0],font_style="Button",on_release=partial(self.display_submenu,c[0],res_id))
            item.add_widget(IconRightWidget(icon="plus"))

            self.ids.food_menu.add_widget(item)

    def display_submenu(self,category,res_id,*args):
        self.ids.submenu.clear_widgets()
        sql=f"Select * from food_items Where Restaurant_Id='{res_id}' and Category='{category}'"
        cursor.execute(sql)
        res=cursor.fetchall()

        for item in res:
            c=FoodCard(orientation='horizontal',elevation=40,ripple_behavior=True,size_hint=(1,None),height="100dp")
            
            
            c.add_widget(Image(texture=CoreImage(BytesIO(item[5]),ext="jpg").texture,size_hint=(0.9,0.9 ),allow_stretch=True))
            c.add_widget(MDLabel(text=str(item[1]),halign="center",theme_text_color="Custom",text_color=(1,1,1,1),font_style="H6"))

            if item[6]=="1":
                c.add_widget(Image(source="images/veg.png"))
            elif item[6]=="0":
                c.add_widget(Image(source="images/nonveg.png"))
            self.ids.submenu.add_widget(c)
        self.ids.orders_sm.current="submenu"
    def search(self,text,*args):
        pass
    def display_restaurants(self,*args):
        self.ids.res_food_list.clear_widgets()
        
        mydb.commit()
        sql="Select Restaurant_Id,Name,Image from restaurants"
        cursor.execute(sql)
        res=cursor.fetchall()

        
        for i in res:
            c=MyCard(orientation='horizontal',elevation=40,ripple_behavior=True,size_hint=(1,None),height="100dp",on_release=partial(self.display_food_menu,str(i[0])))
            
            
            c.add_widget(Image(texture=CoreImage(BytesIO(i[2]),ext="jpg").texture,size_hint=(0.9,0.9 ),allow_stretch=True))
            c.add_widget(MDLabel(text=str(i[1]),halign="center",theme_text_color="Custom",text_color=(1,1,1,1),font_style="H6"))

            self.ids.res_food_list.add_widget(c)


        
    

        

class MainApp(MDApp):
    def build(self):
        return User_Screen()

#MainApp().run()
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from config import pass_cursor
import datetime
from hashlib import sha256
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineListItem
from kivy.metrics import dp
#from loginscreen import pass_cursor
cursor,mydb=pass_cursor()

Builder.load_file('register_for_users_screen.kv')

class Register_User_Screen(Screen):
    def __init__(self,**kwargs):
        super(Register_User_Screen,self).__init__(**kwargs)
        mydb.commit()
        sql="Select Distinct city_state from cities"
        cursor.execute(sql)
        res=cursor.fetchall()
        self.city_menu = MDDropdownMenu(
            caller=self.ids.city,
            items=[],
            position="center",
            width_mult=8,
        )
        self.state_menu_items=[
            {
                "viewclass": "OneLineListItem",
                
                "text": f"{i[0]}",
                "height": dp(56),
                "on_release": lambda x=f"{i[0]}": self.set_state_item(x),
            } for i in res
        ]
        self.state_menu = MDDropdownMenu(
            caller=self.ids.state,
            items=self.state_menu_items,
            position="center",
            width_mult=8,
        )

        self.state_menu.bind()

        

        



    def set_state_item(self, text_item):
        self.ids.state.set_item(text_item)
        self.ids.state.text=text_item
        self.state_menu.dismiss()

        sql=f"Select Distinct city_name from cities Where city_state='{text_item}' "
        cursor.execute(sql)
        cities=cursor.fetchall()

        self.city_menu_items=[
            {
                "viewclass": "OneLineListItem",
                
                "text": f"{i[0]}",
                "height": dp(56),
                "on_release": lambda x=f"{i[0]}": self.set_city_item(x),
            } for i in cities
        ]
        self.city_menu = MDDropdownMenu(
            caller=self.ids.city,
            items=self.city_menu_items,
            position="center",
            width_mult=8,
        )

        self.city_menu.bind()
    
    def set_city_item(self, text_item):
        self.ids.city.set_item(text_item)
        self.ids.city.text=text_item
        self.city_menu.dismiss()

    def nav_to_login(self,*args):
        self.ids.name.text=""
        self.ids.mobile.text=""
        self.ids.address.text=""
        self.ids.city.text="City"
        self.ids.state.text="State"
        self.ids.pincode.text=""
        self.ids.message.text=""

        self.ids.password.text=""

        self.parent.current="login"
    def register(self,*args):
        self.ids.message.text=""
        mydb.commit()
        if self.ids.name.text and self.ids.mobile.text and self.ids.address.text and self.ids.city.text!="City" and self.ids.state.text!="State" and self.ids.pincode.text and self.ids.password.text:
            sql=f"Select Mobile from users Where Mobile='{self.ids.mobile.text}'"
            cursor.execute(sql)
            if cursor.fetchall()==[]:
                sql=f"Select Mobile from restaurants Where Mobile='{self.ids.mobile.text}'"
                cursor.execute(sql)
                if cursor.fetchall()==[]:
                    if self.ids.mobile.text.isnumeric() and len(self.ids.mobile.text)>=10:
                        date=datetime.datetime.now().strftime("%Y-%m-%d")
                        time=str(datetime.datetime.now().strftime("%I:%M:%S%p")).lower()

                        sql=f"Insert Into users (Date,Time,Name,Mobile,Password,Address,City,State,Pincode) Values ('{date}','{time}','{self.ids.name.text}','{self.ids.mobile.text}','{sha256(self.ids.password.text.encode()).hexdigest()}','{self.ids.address.text}','{self.ids.city.text}','{self.ids.state.text}','{self.ids.pincode.text}')"
                        cursor.execute(sql)
                        mydb.commit()
                        self.nav_to_login()
                    else:
                        self.ids.message.text="[color=#e40017][*][/color] Invalid Mobile Number"
                else:
                    self.ids.message.text='[color=#e40017][*][/color] Mobile Number Already Registered '
            else:
                self.ids.message.text='[color=#e40017][*][/color] Mobile Number Already Registered '
        else:
            self.ids.message.text="[color=#e40017][*][/color] Enter All Details"

class MainApp(MDApp):
    def build(self):
        return Register_User_Screen()

#MainApp().run()
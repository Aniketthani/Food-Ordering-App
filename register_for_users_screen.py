from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from config import connect_to_database
import datetime
from hashlib import sha256

cursor,mydb=connect_to_database()

Builder.load_file('register_for_users_screen.kv')

class Register_User_Screen(Screen):
    def nav_to_login(self,*args):
        self.ids.name.text=""
        self.ids.mobile.text=""
        self.ids.address.text=""
        self.ids.city.text=""
        self.ids.state.text=""
        self.ids.pincode.text=""
        self.ids.message.text=""

        self.ids.password.text=""

        self.parent.current="login"
    def register(self,*args):
        self.ids.message.text=""
        mydb.commit()
        if self.ids.name.text and self.ids.mobile.text and self.ids.address.text and self.ids.city.text and self.ids.state.text and self.ids.pincode.text and self.ids.password.text:
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
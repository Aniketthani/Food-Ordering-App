from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from hashlib import sha256
from config import connect_to_database

cursor,mydb=connect_to_database()


Builder.load_file('loginscreen.kv')

class LoginScreen(Screen):

    def nav_to_userscreen(self,*args):
        self.ids.mobile.text=""
        self.ids.password.text=""
        self.ids.message.text=""

        self.parent.current="userscreen"
    def nav_to_restaurantscreen(self,name,Id,*args):
        self.ids.mobile.text=""
        self.ids.password.text=""
        self.ids.message.text=""

        self.parent.current="restaurantscreen"
        self.parent.restaurantscreen.r_name=name
        self.parent.restaurantscreen.Id=str(Id)

    def login(self,*args):
        self.ids.message.text=""
        if self.ids.mobile.text and self.ids.password.text:
            if self.ids.mobile.text.isnumeric() and len(self.ids.mobile.text)>=10:
                mydb.commit()
                sql=f"Select * from users Where Mobile='{self.ids.mobile.text}' and Password='{sha256(self.ids.password.text.encode()).hexdigest()}'"
                cursor.execute(sql)
                if cursor.fetchall()!=[]:
                    self.nav_to_userscreen()
                else:
                    sql=f"Select * from restaurants Where Mobile='{self.ids.mobile.text}' and Password='{sha256(self.ids.password.text.encode()).hexdigest()}'"
                    cursor.execute(sql)
                    res=cursor.fetchall()
                    if res!=[]:
                        self.nav_to_restaurantscreen(res[0][3],res[0][0])
                    else:
                        self.ids.message.text="[color=#e40017][*][/color] Invalid Phone Number or Password"
            else:
                self.ids.message.text="[color=#e40017][*][/color] Invalid Mobile Number "
        else:
            self.ids.message.text="[color=#e40017][*][/color] Please Enter Details"

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette="Red"
        self.theme_cls.theme_style="Light"

        return LoginScreen()
     

#MainApp().run()

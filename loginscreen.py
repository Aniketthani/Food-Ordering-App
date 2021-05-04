from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from hashlib import sha256
from config import connect_to_database
from kivymd.toast import toast


cursor,mydb=connect_to_database()


Builder.load_file('loginscreen.kv')


class LoginScreen(Screen):

    def nav_to_userscreen(self,u_id,u_name,city,state,*args):
        self.ids.mobile.text=""
        self.ids.password.text=""
        self.ids.message.text=""

        self.parent.current="userscreen"
        self.parent.userscreen.userid=str(u_id)
        self.parent.userscreen.username=u_name
        self.parent.userscreen.city=city
        self.parent.userscreen.state=state
        self.parent.userscreen.display_restaurants()

        with open("session.txt","w") as f:
            matter=f"""{u_id}-{u_name}-u-{city}-{state}"""
            f.write(matter)
            f.close()
        
    def nav_to_restaurantscreen(self,name,Id,city,state,*args):
        self.ids.mobile.text=""
        self.ids.password.text=""
        self.ids.message.text=""

        self.parent.current="restaurantscreen"
        self.parent.restaurantscreen.r_name=name
        self.parent.restaurantscreen.Id=str(Id)
        self.parent.restaurantscreen.load_order_list()
        self.parent.datepicker.bind(on_save=self.parent.restaurantscreen.save_date,on_cancel=self.parent.restaurantscreen.cancel_date)
        self.parent.restaurantscreen.city=city
        self.parent.restaurantscreen.state=state
        with open("session.txt","w") as f:
            matter=f"""{Id}-{name}-r-{city}-{state}"""
            f.write(matter)
            f.close()

    def login(self,*args):
        self.ids.message.text=""
        if self.ids.mobile.text and self.ids.password.text:
            if self.ids.mobile.text.isnumeric() and len(self.ids.mobile.text)>=10:
                mydb.commit()
                sql=f"Select * from users Where Mobile='{self.ids.mobile.text}' and Password='{sha256(self.ids.password.text.encode()).hexdigest()}'"
                cursor.execute(sql)
                res=cursor.fetchall()
                if res!=[]:
                    self.nav_to_userscreen(res[0][0],res[0][3],res[0][7],res[0][8])
                else:
                    sql=f"Select * from restaurants Where Mobile='{self.ids.mobile.text}' and Password='{sha256(self.ids.password.text.encode()).hexdigest()}'"
                    cursor.execute(sql)
                    res=cursor.fetchall()
                    if res!=[]:
                        self.nav_to_restaurantscreen(res[0][3],res[0][0],res[0][5],res[0][6])
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

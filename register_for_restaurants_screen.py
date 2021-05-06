from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from config import pass_cursor
import datetime
from hashlib import sha256
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineListItem
from kivy.metrics import dp
import os
from PIL import Image
#from loginscreen import pass_cursor
try:
    from android.storage import primary_external_storage_path
    primary_ext_storage = primary_external_storage_path()
except:
    primary_ext_storage="/"

cursor,mydb=pass_cursor()

Builder.load_file('register_for_restaurants_screen.kv')

class Register_Restaurant_Screen(Screen):
    def __init__(self,**kwargs):
        super(Register_Restaurant_Screen,self).__init__(**kwargs)
        Window.bind(on_keyboard=self.events)
        self.image_path=""
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=True,
        )

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

    def size_of_img(self,file):
        return os.stat(file).st_size

    def file_manager_open(self):
        self.file_manager.show(primary_ext_storage)  # output manager to the screen
        self.manager_open = True


    def select_path(self, path):
        '''It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        '''

        try:
            extension=path.split(".")[1]
            if extension=="jpg" or extension=="png" or extension=="jpeg":
                size=self.size_of_img(path)
                if size <=300000:

                    self.image_path=path
                    self.ids.choose_image_button.text=path.split(".")[0].split("/")[-1]+"."+extension
                    self.exit_manager()
                    Image.open(path).save("out."+ extension,optimized=True,quality=7)
                    self.image_path="out."+extension

                else:
                    toast("Image size should not be more than 300Kb")

            else:
                toast("please select a valid image file")
        except:
            toast("please select a valid image file")

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True

    def nav_to_login(self,*args):
        self.ids.name.text=""
        self.ids.mobile.text=""
        self.ids.address.text=""
        self.ids.city.text="City"
        self.ids.state.text="State"
        self.ids.pincode.text=""
        self.ids.message.text=""
        
        self.ids.password.text=""
        self.ids.choose_image_button.text="Choose Image"
        self.image_path=""

        self.parent.current="login"

    def register(self,*args):
        self.ids.message.text=""
        mydb.commit()
        if self.ids.name.text and self.ids.mobile.text and self.ids.address.text and self.ids.city.text!="City" and self.ids.state.text!="State" and self.ids.pincode.text and self.ids.password.text and self.image_path:
            sql=f"Select Mobile from restaurants Where Mobile='{self.ids.mobile.text}'"
            cursor.execute(sql)
            if cursor.fetchall()==[]:
                sql=f"Select Mobile from users Where Mobile='{self.ids.mobile.text}'"
                cursor.execute(sql)
                if cursor.fetchall()==[]:

                    if self.ids.mobile.text.isnumeric() and len(self.ids.mobile.text)>=10:
                        date=datetime.datetime.now().strftime("%Y-%m-%d")
                        time=str(datetime.datetime.now().strftime("%I:%M:%S%p")).lower()

                        sql=f"Insert Into restaurants (Date,Time,Name,Address,City,State,Pincode,Mobile,Password,Image) Values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        with open(self.image_path,"rb") as f:
                            bdata=f.read()
                        cursor.execute(sql,(date,time,self.ids.name.text,self.ids.address.text,self.ids.city.text,self.ids.state.text,self.ids.pincode.text,self.ids.mobile.text,sha256(self.ids.password.text.encode()).hexdigest(),bdata))
                        mydb.commit()
                        os.remove(self.image_path)
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
        return Register_Restaurant_Screen()

#MainApp().run()
from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from config import connect_to_database
import datetime
from hashlib import sha256
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast

try:
    from android.storage import primary_external_storage_path
    primary_ext_storage = primary_external_storage_path()
except:
    primary_ext_storage="/"

cursor,mydb=connect_to_database()

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
                self.image_path=path
                self.ids.choose_image_button.text=path.split(".")[0].split("/")[-1]+"."+extension
                self.exit_manager()

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
        self.ids.city.text=""
        self.ids.state.text=""
        self.ids.pincode.text=""
        self.ids.message.text=""
        
        self.ids.password.text=""
        self.ids.choose_image_button.text="Choose Image"
        self.image_path=""

        self.parent.current="login"

    def register(self,*args):
        self.ids.message.text=""
        mydb.commit()
        if self.ids.name.text and self.ids.mobile.text and self.ids.address.text and self.ids.city.text and self.ids.state.text and self.ids.pincode.text and self.ids.password.text and self.image_path:
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
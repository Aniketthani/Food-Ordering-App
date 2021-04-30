from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import ObjectProperty,StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from config import connect_to_database
from edit_food_item_screen import Edit_Food_Item_Screen
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
try:
    from android.storage import primary_external_storage_path
    primary_ext_storage = primary_external_storage_path()
except:
    primary_ext_storage="/"


cursor,mydb=connect_to_database()

Builder.load_file('restaurantscreen.kv')

class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

class Restaurant_Screen(Screen):
    r_name=StringProperty()
    Id=StringProperty()
    veg=True
    item_list=[]
    item_selected=""

    
    def load_dropdown_items(self,*args):
        mydb.commit()
        sql="Select Category from food_categories"
        cursor.execute(sql)
        self.item_list=cursor.fetchall()
        self.item_selected=""
        

        self.menu_items = [
            {
                "viewclass": "OneLineIconListItem",
                
                "text": f"{i[0]}",
                "on_release": lambda x=f"{i[0]}": self.set_item(x),
            } for i in self.item_list]
        self.menu = MDDropdownMenu(
            caller=self.ids.field,
            items=self.menu_items,
            position="center",
            width_mult=7,
        )
        
    def set_item(self, text__item):
        self.ids.field.text = text__item
        self.item_selected=text__item
        self.menu.dismiss()


    def __init__(self,**kwargs):
        super(Restaurant_Screen,self).__init__(**kwargs)
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.image_path=""
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=True,
        )

        self.load_dropdown_items()


    #def search_category(self,text,*args):
    #    sql=f"Select Category from food_categories Where Category Like '%{text}%'"
    #    cursor.execute(sql)
    #    self.item_list=cursor.fetchall()
#
    #    self.menu_items = [
    #        {
    #            "viewclass": "OneLineIconListItem",
    #            "height": dp(56),
    #            "text": f"{i[0]}",
    #            "on_release": lambda x=f"{i[0]}": self.set_item(x),
    #        } for i in self.item_list]
#
    #    self.menu.items=self.menu_items
        
        
        


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
                self.ids.file_manager_button.text=path.split(".")[0].split("/")[-1]+"."+extension
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

    def convert_to_binary(self,filename):
        with open(filename,"rb") as file:
            bdata=file.read()
        return bdata

    def add_food(self,*args):
        if self.ids.f_name.text and self.ids.f_desc.text and self.ids.f_price.text and (self.ids.veg.active or self.ids.nonveg.active) and self.ids.field.text!="Category":
            if self.ids.f_price.text.isnumeric():
                if self.image_path :
                    photo=self.convert_to_binary(self.image_path)
                    sql="Insert Into food_items (F_Name,Restaurant_Id,Price,Description,Image,Veg,Category) Values(%s,%s,%s,%s,%s,%s,%s)"

                    cursor.execute(sql,(self.ids.f_name.text,self.Id,self.ids.f_price.text,self.ids.f_desc.text,photo,int(self.veg),self.item_selected))
                    mydb.commit()
                    toast("Food Item Added Successfully")
                    self.ids.f_name.text=""
                    self.ids.f_desc.text=""
                    self.ids.f_price.text=""
                    self.ids.veg.active=True
                    self.veg=True
                    self.ids.field.text="Category"
                    self.ids.file_manager_button.text="Choose Image"
                    self.image_path=""
                    
                else:
                    toast("Please select a image")
            else:
                toast("Please enter a valid price")
        else:
            toast("Please fill all the details ")
        
    
        


class MainApp(MDApp):
    def build(self):
        return Restaurant_Screen()

#MainApp().run()
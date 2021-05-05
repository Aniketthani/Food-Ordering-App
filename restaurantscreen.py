from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import ObjectProperty,StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from config import pass_cursor
from edit_food_item_screen import Edit_Food_Item_Screen
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
from datetime import datetime
from kivymd.uix.list import OneLineAvatarIconListItem,IconLeftWidget
from functools import partial
from datatables import MDDataTable
from kivy.clock import Clock
#from loginscreen import pass_cursor
try:
    from android.storage import primary_external_storage_path
    primary_ext_storage = primary_external_storage_path()
except:
    primary_ext_storage="/"



cursor,mydb=pass_cursor()

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
    city=StringProperty()
    state=StringProperty()
    
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
    
    def logout(self,*args):
        self.parent.current="login"
        with open("session.txt","w") as f:
            f.write("")
            f.close()

    def save_date(self,instance, value, date_range):
        self.ids.choose_date_btn.text=str(value)

    def cancel_date(self, instance, value):
        instance.dismiss()
    
    def load_dispatched_order_list(self,from_sub_btn,*args):
        if not from_sub_btn:
            self.ids.choose_date_btn.text="Choose Date"
            self.ids.dispatched_order_list.clear_widgets()
        if self.ids.choose_date_btn.text!="Choose Date" and from_sub_btn:
            mydb.commit()
            
        
            sql=f"Select * from orders Where Restaurant_Id='{self.Id}' and Date='{self.ids.choose_date_btn.text}' and Dispatched='1'"

            cursor.execute(sql)
            res=cursor.fetchall()

            self.ids.dispatched_order_list.clear_widgets()
            for order in res:
                item=OneLineAvatarIconListItem(text=f"Order No : {order[0]}",on_release=partial(self.show_order_details,order,True))
                item.add_widget(IconLeftWidget(icon="receipt"))
                self.ids.dispatched_order_list.add_widget(item)
        elif self.ids.choose_date_btn.text=="Choose Date" and from_sub_btn:
            
            toast("Please select date")
            self.ids.dispatched_order_list.clear_widgets()
    



        
    def load_order_list(self,*args):
        mydb.commit()
        date=datetime.now().strftime("%Y-%m-%d")
        
        sql=f"Select * from orders Where Restaurant_Id='{self.Id}' and Date='{date}' and Dispatched='0'"

        cursor.execute(sql)
        res=cursor.fetchall()

        self.ids.order_list.clear_widgets()
        for order in res:
            item=OneLineAvatarIconListItem(text=f"Order No : {order[0]}",on_release=partial(self.show_order_details,order,False))
            item.add_widget(IconLeftWidget(icon="receipt"))
            self.ids.order_list.add_widget(item)
        
        Clock.schedule_once(self.load_order_list,5)

    def show_order_details(self,order,dispatched,*args):
        self.ids.screen_manager.current="particular_order_screen"
        sql=f"Select * from users where Id='{order[8]}'"
        cursor.execute(sql)
        res=cursor.fetchall()[0]

        self.ids.order_header_details.text=f"""ONO : {order[0]}  Customer : {res[3]} \n Mobile : {res[4]}  Address : {res[6]}\n
City : {res[7]}  State : {res[8]} \n Pincode : {res[9]}"""

        self.ids.total_bill.text=f"Total : Rs {order[7]}"
        
        f_items=tuple(order[5].split("-"))
        f_quantity=order[6].split("-")

        if len(f_items)==1:
            sql=f"Select F_Name,Price from food_items Where F_Id='{f_items[0]}' "
        else:
            sql=f"Select F_Name,Price from food_items Where F_Id In {f_items}"

        cursor.execute(sql)
        res=cursor.fetchall()

        rows=[]
        
        for i in range(len(f_items)):
            t=(res[i][0],res[i][1],f_quantity[i],int(res[i][1])*int(f_quantity[i]))
            rows.append(t)
        rows.append(("","","",""))





        try:
            self.ids.particular_order_screen.remove_widget(self.ordertable)
        except:
            pass
        self.ordertable=MDDataTable(size_hint=(0.9,0.5),column_data=[
                ("Food", dp(20)),
                ("Price", dp(15)),
                
                ("Quantity", dp(15)),
                ("Total", dp(15)),
                
            ],
            pos_hint={'top':0.5,'center_x':0.5},row_data=rows
            )
        self.ids.particular_order_screen.add_widget(self.ordertable)

        if not  dispatched:
            self.ids.dispatch_order_btn.disabled=False

            self.ids.dispatch_order_btn.on_release=partial(self.dispatch_order,order[0])
            self.ids.backbtn.on_release=partial(self.back_navigate,"order_screen")
        else:
            self.ids.dispatch_order_btn.disabled=True

            self.ids.backbtn.on_release=partial(self.back_navigate,"dispatched_orders")
    
    def back_navigate(self,screen,*args):
        self.ids.screen_manager.current=screen

    def dispatch_order(self,ono,*args):
        sql=f"Update orders set Dispatched='1' Where ONO='{ono}'"
        cursor.execute(sql)
        mydb.commit()
        self.ids.dispatch_order_btn.disabled=True
        self.ids.screen_manager.current="order_screen"
        toast(f"Order No {ono} dispatched successfully")
        

    def load_dropdown_items(self,*args):
        self.ids.f_name.text=""
        self.ids.f_desc.text=""
        self.ids.f_price.text=""
        self.ids.field.text="Category"
        self.ids.file_manager_button.text="Choose Image"
        self.image_path=""
        self.ids.veg.active=True
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
                    sql=f"Select City,State from restaurants Where Restaurant_Id='{self.Id}'"
                    cursor.execute(sql)
                    city=cursor.fetchall()[0]
                    state=city[1]
                    city=city[0]
                    photo=self.convert_to_binary(self.image_path)
                    sql="Insert Into food_items (F_Name,Restaurant_Id,Price,Description,Image,Veg,Category,City,State) Values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"

                    cursor.execute(sql,(self.ids.f_name.text,self.Id,self.ids.f_price.text,self.ids.f_desc.text,photo,int(self.veg),self.item_selected,city,state))
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
        
    
        




